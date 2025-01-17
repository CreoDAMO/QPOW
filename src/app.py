from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from src.quantum_services import
QFCOnramper, NFTMarketplace, QKDManager, QuantumAIOptimizer
from src.core import Blockchain
import logging
import os
import time

# -------------------- Configure Logging --------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# -------------------- Initialize Flask App --------------------

app = Flask(__name__)
CORS(app)


# -------------------- Load Configuration --------------------

DEBUG_MODE = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1", "t"]
API_KEY = os.getenv("API_KEY", "default-api-key")


# -------------------- Core Components --------------------

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


# -------------------- Middleware --------------------

@app.before_request
def check_api_key():
    """Middleware to check API key for secure routes."""
    if request.endpoint not in ["health_check"]:
        api_key = request.headers.get("X-API-KEY")
        if api_key != API_KEY:
            logger.warning("Unauthorized access attempt detected.")
            abort(401, description="Unauthorized")


# -------------------- API Routes --------------------

@app.route("/v1/nft/teleport", methods=["POST"])
def teleport_nft():
    """Teleport an NFT from one user to another."""
    start_time = time.time()
    data = request.json
    validate_request(data, ["token_id", "sender", "recipient"])

    try:
        nft_marketplace.teleport_nft(
            data["token_id"],
            data["sender"],
            data["recipient"]
        )
        logger.info(
            f"NFT {data['token_id']} teleported from "
            f"{data['sender']} to {data['recipient']}."
        )
        total_time = time.time() - start_time
        logger.info(f"Request processed in {total_time:.4f} seconds.")
        return jsonify({"success": True, "message": "NFT teleported successfully."})
    except ValueError as e:
        logger.error(f"Error in teleport_nft: {str(e)}")
        return jsonify(
            {"success": False,
             "error": "An error occurred while processing your request."}), 400


@app.route("/v1/onramp/buy", methods=["POST"])
def buy_qfc():
    """Buy QFC coins using fiat currency."""
    start_time = time.time()
    data = request.json
    validate_request(data, ["user", "fiat_amount", "currency"])

    try:
        onramper.buy_qfc(
            data["user"],
            data["fiat_amount"],
            data["currency"]
        )
        logger.info(
            f"User {data['user']} bought {data['fiat_amount']} "
            f"{data['currency']} worth of QFC coins."
        )
        total_time = time.time() - start_time
        logger.info(
            f"Request processed in {total_time:.4f} seconds.")
        return jsonify(
            {"success": True, "message": "Fiat converted to QFC coins successfully."})
    except ValueError as e:
        logger.error(f"Error in buy_qfc: {str(e)}")
        return jsonify(
            {"success": False,
             "error": "An error occurred while processing your request."}), 400


@app.route("/v1/qkd/distribute", methods=["POST"])
def distribute_qkd_key():
    """Distribute a QKD key between two users."""
    start_time = time.time()
    data = request.json
    validate_request(data, ["sender", "recipient"])

    try:
        key = qkd_manager.distribute_key(
            data["sender"],
            data["recipient"]
        )
        logger.info(
            f"QKD key distributed between {data['sender']} and {data['recipient']}."
        )
        total_time = time.time() - start_time
        logger.info(f"Request processed in {total_time:.4f} seconds.")
        return jsonify({"success": True, "message": f"QKD key distributed: {key}"})
    except ValueError as e:
        logger.error(f"Error in distribute_qkd_key: {str(e)}")
        return jsonify(
            {"success": False,
             "error": "An error occurred while distributing the QKD key."}), 400


@app.route("/v1/qkd/teleport", methods=["POST"])
def teleport_qkd_key():
    """Teleport a QKD key using quantum teleportation."""
    start_time = time.time()
    data = request.json
    validate_request(data, ["sender", "recipient"])

    try:
        qkd_manager.teleport_qkd_key(
            data["sender"],
            data["recipient"]
        )
        logger.info(
            f"QKD key teleported between {data['sender']} and {data['recipient']}."
        )
        total_time = time.time() - start_time
        logger.info(f"Request processed in {total_time:.4f} seconds.")
        return jsonify({"success": True, "message": "QKD key teleported successfully."})
    except ValueError as e:
        logger.error(f"Error in teleport_qkd_key: {str(e)}")
        return jsonify(
            {"success": False,
             "error": "An error occurred while teleporting the QKD key."}), 400


@app.route("/v1/shard/optimize", methods=["POST"])
def optimize_shard_allocation():
    """Optimize shard allocation for a set of transactions."""
    start_time = time.time()
    data = request.json
    validate_request(data, ["transaction_details"])

    try:
        shard_allocations = quantum_ai_optimizer.optimize_shard_allocation(
            data["transaction_details"]
        )
        logger.info(f"Shard allocations: {shard_allocations}")
        total_time = time.time() - start_time
        logger.info(f"Request processed in {total_time:.4f} seconds.")
        return jsonify({"success": True, "shard_allocations": shard_allocations})
    except ValueError as e:
        logger.error(f"Error in optimize_shard_allocation: {str(e)}")
        return jsonify(
            {"success": False,
             "error": "An error occurred while optimizing shard allocation."}), 400


@app.route("/v1/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "Healthy", "timestamp": time.time()}), 200


# -------------------- Error Handlers --------------------

@app.errorhandler(400)
def handle_bad_request(error):
    """Handle 400 Bad Request errors."""
    logger.error(f"Bad Request: {error.description}")
    return jsonify({"success": False, "error": error.description}), 400


@app.errorhandler(401)
def handle_unauthorized(error):
    """Handle 401 Unauthorized errors."""
    logger.warning(f"Unauthorized: {error.description}")
    return jsonify({"success": False, "error": error.description}), 401


@app.errorhandler(404)
def handle_not_found(error):
    """Handle 404 Not Found errors."""
    logger.error(f"Not Found: {error.description}")
    return jsonify({"success": False, "error": error.description}), 404


@app.errorhandler(500)
def handle_internal_server_error(error):
    """Handle 500 Internal Server errors."""
    logger.critical(f"Internal Server Error: {error}")
    return jsonify({"success": False,
                    "error": "Internal server error occurred."}), 500


# -------------------- Main Function --------------------

if __name__ == "__main__":
    logger.info("Starting the QuantumFuse Flask app...")
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=5000)
