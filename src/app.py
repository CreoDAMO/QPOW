from flask import Flask, jsonify, request
from src.services import QFCOnramper, NFTMarketplace, QKDManager, QuantumAIOptimizer
from src.core import Blockchain, Transaction
import logging

app = Flask(__name__)

# Initialize the required services
blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
nft_marketplace = NFTMarketplace(blockchain)
onramper = QFCOnramper(blockchain, analytics=None, compliance=None)
qkd_manager = QKDManager()
quantum_ai_optimizer = QuantumAIOptimizer()

@app.route('/nft/teleport', methods=['POST'])
def teleport_nft():
    data = request.json
    try:
        nft_marketplace.teleport_nft(data["token_id"], data["sender"], data["recipient"])
        return jsonify({"success": True, "message": "NFT teleported successfully."})
    except ValueError as e:
        logging.error(f"Error in teleport_nft: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."})

@app.route('/onramp/buy', methods=['POST'])
def buy_qfc():
    data = request.json
    try:
        onramper.buy_qfc(data["user"], data["fiat_amount"], data["currency"])
        return jsonify({"success": True, "message": "Fiat converted to QFC successfully."})
    except ValueError as e:
        logging.error(f"Error in buy_qfc: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."})

@app.route('/qkd/distribute', methods=['POST'])
def distribute_qkd_key():
    data = request.json
    try:
        key = qkd_manager.distribute_key(data["sender"], data["recipient"])
        return jsonify({"success": True, "message": f"QKD key distributed: {key}"})
    except ValueError as e:
        logging.error(f"Error in distribute_qkd_key: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."})

@app.route('/qkd/teleport', methods=['POST'])
def teleport_qkd_key():
    data = request.json
    try:
        qkd_manager.teleport_qkd_key(data["sender"], data["recipient"])
        return jsonify({"success": True, "message": "QKD key teleported successfully."})
    except ValueError as e:
        logging.error(f"Error in teleport_qkd_key: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."})

@app.route('/shard/optimize', methods=['POST'])
def optimize_shard_allocation():
    data = request.json
    try:
        shard_allocations = quantum_ai_optimizer.optimize_shard_allocation(data["transaction_details"])
        return jsonify({"success": True, "shard_allocations": shard_allocations})
    except ValueError as e:
        logging.error(f"Error in optimize_shard_allocation: {str(e)}")
        return jsonify({"success": False, "error": "An internal error has occurred."})

if __name__ == '__main__':
    app.run(debug=True)
