from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from src.services import QFCOnramper, NFTMarketplace, QKDManager, QuantumAIOptimizer
from src.core import Blockchain, Transaction
import logging
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize the Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Load configuration from environment variables
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
API_KEY = os.getenv('API_KEY', 'default-api-key')

# Initialize the core components and services
blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
nft_marketplace = NFTMarketplace(blockchain)
onramper = QFCOnramper(blockchain, analytics=None, compliance=None)
qkd_manager = QKDManager()
quantum_ai_optimizer = QuantumAIOptimizer()


# -------------------- Helper Functions --------------------

def validate_request(data, required_fields):
    """Validate that the required fields exist in the request data."""
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field: {field}")
            abort(400, description=f"Missing required field: {field}")

@app.before_request
def check_api_key():
    """Middleware to check API key for secure routes."""
    if request.endpoint not in ['health_check']:
        api_key = request.headers.get('X-API-KEY')
        if api_key != API_KEY:
            logger.warning("Unauthorized access attempt detected.")
            abort(401, description="Unauthorized")


# -------------------- API Routes --------------------

@app.route('/v1/nft/teleport', methods=['POST'])
def teleport_nft():
    """Teleport an NFT from one user to another."""
    data = request.json
    validate_request(data, ["token_id", "sender", "recipient"])
    try:
        nft_marketplace.teleport_nft(data["token_id"], data["sender"], data["recipient"])
        logger.info(f"NFT {data['token_id']} teleported from {data['sender']} to {data['recipient']}.")
        return jsonify({"success": True, "message": "NFT teleported successfully."})
    except ValueError as e:
        logger.error(f"Error in teleport_nft: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."}), 400

@app.route('/v1/onramp/buy', methods=['POST'])
def buy_qfc():
    """Buy QFC tokens using fiat currency."""
    data = request.json
    validate_request(data, ["user", "fiat_amount", "currency"])
    try:
        onramper.buy_qfc(data["user"], data["fiat_amount"], data["currency"])
        logger.info(f"User {data['user']} bought {data['fiat_amount']} {data['currency']} worth of QFC.")
        return jsonify({"success": True, "message": "Fiat converted to QFC successfully."})
    except ValueError as e:
        logger.error(f"Error in buy_qfc: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."}), 400

@app.route('/v1/qkd/distribute', methods=['POST'])
def distribute_qkd_key():
    """Distribute a QKD key between two users."""
    data = request.json
    validate_request(data, ["sender", "recipient"])
    try:
        key = qkd_manager.distribute_key(data["sender"], data["recipient"])
        logger.info(f"QKD key distributed between {data['sender']} and {data['recipient']}.")
        return jsonify({"success": True, "message": f"QKD key distributed: {key}"})
    except ValueError as e:
        logger.error(f"Error in distribute_qkd_key: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."}), 400

@app.route('/v1/qkd/teleport', methods=['POST'])
def teleport_qkd_key():
    """Teleport a QKD key using quantum teleportation."""
    data = request.json
    validate_request(data, ["sender", "recipient"])
    try:
        qkd_manager.teleport_qkd_key(data["sender"], data["recipient"])
        logger.info(f"QKD key teleported between {data['sender']} and {data['recipient']}.")
        return jsonify({"success": True, "message": "QKD key teleported successfully."})
    except ValueError as e:
        logger.error(f"Error in teleport_qkd_key: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."}), 400

@app.route('/v1/shard/optimize', methods=['POST'])
def optimize_shard_allocation():
    """Optimize shard allocation for a set of transactions."""
    data = request.json
    validate_request(data, ["transaction_details"])
    try:
        shard_allocations = quantum_ai_optimizer.optimize_shard_allocation(data["transaction_details"])
        logger.info(f"Shard allocations: {shard_allocations}")
        return jsonify({"success": True, "shard_allocations": shard_allocations})
    except ValueError as e:
        logger.error(f"Error in optimize_shard_allocation: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."}), 400

@app.route('/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "Healthy", "timestamp": time.time()}), 200

# -------------------- Main Function --------------------
if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
