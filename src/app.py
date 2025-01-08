from flask import Flask, jsonify, request
from .services import QFCOnramper, NFTMarketplace, QKDManager, QuantumAIOptimizer
from .core import Blockchain, Wallet, Transaction

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
        return jsonify({"success": True, "message": f"NFT teleported successfully."})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/onramp/buy', methods=['POST'])
def buy_qfc():
    data = request.json
    try:
        onramper.buy_qfc(data["user"], data["fiat_amount"], data["currency"])
        return jsonify({"success": True, "message": f"Fiat converted to QFC successfully."})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/qkd/distribute', methods=['POST'])
def distribute_qkd_key():
    data = request.json
    try:
        key = qkd_manager.distribute_key(data["sender"], data["recipient"])
        return jsonify({"success": True, "message": f"QKD key distributed: {key}"})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/qkd/teleport', methods=['POST'])
def teleport_qkd_key():
    data = request.json
    try:
        qkd_manager.teleport_qkd_key(data["sender"], data["recipient"])
        return jsonify({"success": True, "message": f"QKD key teleported successfully."})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/shard/optimize', methods=['POST'])
def optimize_shard_allocation():
    data = request.json
    try:
        shard_allocations = quantum_ai_optimizer.optimize_shard_allocation(data["transaction_details"])
        return jsonify({"success": True, "shard_allocations": shard_allocations})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
