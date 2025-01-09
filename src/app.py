from flask import Flask, jsonify, request
from src.services import QFCOnramper, NFTMarketplace, QKDManager, QuantumAIOptimizer
from src.core import Blockchain

# Initialize Flask app
app = Flask(__name__)

# Initialize services
blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
nft_marketplace = NFTMarketplace(blockchain)
onramper = QFCOnramper(blockchain)
qkd_manager = QKDManager()
quantum_ai_optimizer = QuantumAIOptimizer()

# -------------------- Routes --------------------

@app.route('/nft/teleport', methods=['POST'])
def teleport_nft():
    """Handle NFT teleportation requests."""
    data = request.json
    try:
        token_id = data["token_id"]
        sender = data["sender"]
        recipient = data["recipient"]
        nft_marketplace.teleport_nft(token_id, sender, recipient)
        return jsonify({"success": True, "message": "NFT teleported successfully."}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/onramp/buy', methods=['POST'])
def buy_qfc():
    """Handle fiat-to-QFC onramp transactions."""
    data = request.json
    try:
        user = data["user"]
        fiat_amount = data["fiat_amount"]
        currency = data["currency"]
        onramper.buy_qfc(user, fiat_amount, currency)
        return jsonify({"success": True, "message": "Fiat converted to QFC successfully."}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/qkd/distribute', methods=['POST'])
def distribute_qkd_key():
    """Distribute a quantum key between two users."""
    data = request.json
    try:
        sender = data["sender"]
        recipient = data["recipient"]
        key = qkd_manager.distribute_key(sender, recipient)
        return jsonify({"success": True, "message": f"QKD key distributed: {key}"}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/qkd/teleport', methods=['POST'])
def teleport_qkd_key():
    """Teleport a QKD key using quantum entanglement."""
    data = request.json
    try:
        sender = data["sender"]
        recipient = data["recipient"]
        qkd_manager.teleport_qkd_key(sender, recipient)
        return jsonify({"success": True, "message": "QKD key teleported successfully."}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/shard/optimize', methods=['POST'])
def optimize_shard_allocation():
    """Optimize shard allocation based on predicted loads."""
    data = request.json
    try:
        transaction_details = data["transaction_details"]
        shard_allocations = quantum_ai_optimizer.optimize_shard_allocation(transaction_details)
        return jsonify({"success": True, "shard_allocations": shard_allocations}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/health', methods=['GET'])
def health_check():
    """Check the health status of the QuantumFuse Blockchain system."""
    return jsonify({"status": "Healthy", "message": "QuantumFuse Blockchain is operational."}), 200


# -------------------- App Initialization --------------------

if __name__ == '__main__':
    app.run(debug=True)
