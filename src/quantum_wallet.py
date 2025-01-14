import logging
from pqc_wrapper import PQCWrapper  # Wrapper for dynamic PQC backend
from argon2 import PasswordHasher
from firebase_admin import messaging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class QuantumWallet:
    """
    A secure wallet supporting post-quantum cryptography with advanced features.
    """

    def __init__(self, user_id: str, password: str, pqc_backend: str = "pqclean"):
        self.user_id = user_id
        self.ph = PasswordHasher()
        self.password_hash = self.ph.hash(password)
        self.pqc = PQCWrapper(pqc_backend)
        self.private_key, self.public_key = self.pqc.generate_keypair()
        self.balance = 0.0
        self.multi_sig_keys = []

    def authenticate(self, password: str) -> bool:
        """Authenticate user with a hashed password."""
        try:
            return self.ph.verify(self.password_hash, password)
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    def add_multi_sig_key(self, public_key: bytes):
        """Add a multi-signature public key."""
        self.multi_sig_keys.append(public_key)

    def sign_transaction(self, recipient: str, amount: float) -> dict:
        """Sign a transaction with post-quantum cryptography."""
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        tx_data = f"{self.user_id}->{recipient}:{amount}".encode()
        signature = self.pqc.sign(tx_data, self.private_key)
        self.balance -= amount
        return {
            "transaction": tx_data.decode(),
            "signature": signature.hex(),
        }

    def verify_transaction(
        self, tx_data: bytes, signature: bytes, public_key: bytes
    ) -> bool:
        """Verify transaction using the selected PQC backend."""
        try:
            return self.pqc.verify(tx_data, signature, public_key)
        except Exception as e:
            logger.error(f"Transaction verification failed: {e}")
            return False

    def notify_transaction(self, message: str):
        """Send a notification about a transaction."""
        notification = messaging.Message(
            notification=messaging.Notification(
                title="Quantum Wallet", 
                body=message
            ),
            topic=self.user_id,
        )
        try:
            messaging.send(notification)
            logger.info(f"Notification sent to {self.user_id}: {message}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
