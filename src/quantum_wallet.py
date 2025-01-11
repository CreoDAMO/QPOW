import hashlib
from pqcrypto.sign.dilithium2 import generate_keypair, sign, verify
from firebase_admin import messaging
from flask import Flask, request, jsonify, abort
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage for wallets
wallets = {}


# -------------------- Quantum Wallet Class --------------------
class QuantumWallet:
    """
    Quantum Wallet with post-quantum cryptography and advanced security features.
    """
    def __init__(self, user_id: str, password: str):
        self.user_id = user_id
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.private_key, self.public_key = generate_keypair()
        self.balance = 0.0
        self.multi_sig_keys = []

    def authenticate(self, password: str) -> bool:
        """Verify user authentication with a hashed password."""
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    def add_multi_sig_key(self, public_key: bytes):
        """Add a public key for multi-signature transactions."""
        self.multi_sig_keys.append(public_key)

    def execute_transaction(self, recipient: str, amount: float):
        """Execute a transaction with a signature."""
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        tx_data = f"{self.user_id}->{recipient}:{amount}".encode()
        signature = sign(tx_data, self.private_key)
        self.balance -= amount
        return {"transaction": tx_data.decode(), "signature": signature.hex()}

    def verify_transaction(self, tx_data: bytes, signature: bytes, public_key: bytes) -> bool:
        """Verify the validity of a transaction signature."""
        try:
            verify(tx_data, signature, public_key)
            return True
        except Exception as e:
            logger.error(f"Transaction verification failed: {e}")
            return False

    def notify_transaction(self, message: str):
        """Send a notification about a transaction."""
        notification = messaging.Message(
            notification=messaging.Notification(title="Quantum Wallet", body=message),
            topic=self.user_id
        )
        messaging.send(notification)
        logger.info(f"Notification sent to {self.user_id}: {message}")


# -------------------- Flask API Endpoints --------------------

@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    """
    Create a new quantum wallet.
    """
    data = request.json
    if "user_id" not in data or "password" not in data:
        logger.error("Missing required fields in wallet creation request.")
        abort(400, description="Missing required fields: user_id or password.")
    
    if data['user_id'] in wallets:
        logger.error(f"Wallet creation failed: User ID {data['user_id']} already exists.")
        return jsonify({"success": False, "error": "User ID already exists."}), 400

    wallet = QuantumWallet(data['user_id'], data['password'])
    wallets[data['user_id']] = wallet
    logger.info(f"Wallet created successfully for user {data['user_id']}.")
    return jsonify({"success": True, "public_key": wallet.public_key.hex()})


@app.route('/wallet/transaction', methods=['POST'])
def execute_transaction():
    """
    Execute a transaction between two wallets.
    """
    data = request.json
    required_fields = ["user_id", "password", "recipient", "amount"]

    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field: {field}")
            abort(400, description=f"Missing required field: {field}")

    wallet = wallets.get(data['user_id'])
    if not wallet or not wallet.authenticate(data['password']):
        logger.error(f"Authentication failed for user {data['user_id']}.")
        return jsonify({"success": False, "error": "Authentication failed."}), 401

    recipient_wallet = wallets.get(data["recipient"])
    if not recipient_wallet:
        logger.error(f"Transaction failed: Recipient {data['recipient']} does not exist.")
        return jsonify({"success": False, "error": "Recipient does not exist."}), 404

    try:
        result = wallet.execute_transaction(data['recipient'], data['amount'])
        recipient_wallet.balance += data['amount']
        wallet.notify_transaction(f"Sent {data['amount']} QFC to {data['recipient']}.")
        recipient_wallet.notify_transaction(f"Received {data['amount']} QFC from {data['user_id']}.")
        logger.info(f"Transaction successful: {data['user_id']} -> {data['recipient']} ({data['amount']} QFC).")
        return jsonify({"success": True, "transaction": result})
    except ValueError as e:
        logger.error(f"Transaction error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/wallet/balance/<user_id>', methods=['GET'])
def get_wallet_balance(user_id):
    """
    Get the balance of a wallet.
    """
    wallet = wallets.get(user_id)
    if not wallet:
        logger.error(f"Balance inquiry failed: Wallet {user_id} does not exist.")
        return jsonify({"success": False, "error": "Wallet does not exist."}), 404

    logger.info(f"Balance inquiry for wallet {user_id}: {wallet.balance} QFC.")
    return jsonify({"success": True, "balance": wallet.balance})

# -------------------- Error Handlers --------------------

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"success": False, "error": error.description}), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"success": False, "error": error.description}), 401

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "error": error.description}), 404

# -------------------- Main Function --------------------
if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
