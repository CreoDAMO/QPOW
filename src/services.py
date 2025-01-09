from flask import Flask, jsonify, request
import requests
import random
import datetime
from typing import Dict, List, Any
from src.core import Blockchain, StateManager
from quantum_lib.teleportation import QuantumTeleportation

# Initialize the blockchain instance globally to avoid redundant creations
blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)

# -------------------- QKDManager --------------------
class QKDManager:
    def __init__(self):
        self.qkd_keys: Dict[str, str] = {}
        self.teleportation = QuantumTeleportation()

    def distribute_key(self, sender: str, recipient: str) -> str:
        key = f"QKD-{random.randint(1000, 9999)}"
        self.qkd_keys[(sender, recipient)] = key
        print(f"QKD key distributed between {sender} and {recipient}.")
        return key

    def get_key(self, sender: str, recipient: str) -> Optional[str]:
        return self.qkd_keys.get((sender, recipient))

    def teleport_qkd_key(self, sender: str, recipient: str) -> bool:
        key = self.get_key(sender, recipient)
        if not key:
            raise ValueError(f"No QKD key found between {sender} and {recipient}.")

        entangled_state = self.teleportation.create_entanglement(sender, recipient)
        if not self.teleportation.validate_teleportation(entangled_state):
            raise ValueError("Quantum teleportation of QKD key failed.")

        print(f"QKD key teleported successfully between {sender} and {recipient}.")
        return True


# -------------------- QuantumAIOptimizer --------------------
class QuantumAIOptimizer:
    def __init__(self):
        self.shard_load_history: Dict[int, List[float]] = {}

    def predict_shard_load(self, shard_id: int) -> float:
        if shard_id not in self.shard_load_history:
            self.shard_load_history[shard_id] = [random.uniform(0, 1) for _ in range(10)]
        return round(sum(self.shard_load_history[shard_id]) / len(self.shard_load_history[shard_id]), 2)

    def optimize_shard_allocation(self, transaction_details: List[Dict[str, Any]]) -> Dict[str, int]:
        shard_allocations = {}
        for tx in transaction_details:
            least_loaded_shard = min(self.shard_load_history.keys(), key=self.predict_shard_load)
            shard_allocations[tx["transaction_id"]] = least_loaded_shard
            self.update_shard_load(least_loaded_shard, 0.1)
        return shard_allocations

    def update_shard_load(self, shard_id: int, load_increment: float):
        if shard_id in self.shard_load_history:
            self.shard_load_history[shard_id].append(load_increment)
            if len(self.shard_load_history[shard_id]) > 10:
                self.shard_load_history[shard_id].pop(0)


# -------------------- QFCOnramper --------------------
class QFCOnramper:
    def __init__(self, blockchain: Blockchain, analytics: Any = None, compliance: Any = None):
        self.blockchain = blockchain
        self.analytics = analytics
        self.compliance = compliance
        self.teleportation = QuantumTeleportation()
        self.exchange_rates_api = "https://api.exchangeratesapi.io/latest?base=USD"
        self.supported_currencies = ["USD", "EUR", "JPY"]
        self.transaction_history: List[Dict[str, Any]] = []

    def fetch_exchange_rates(self) -> Dict[str, float]:
        try:
            response = requests.get(self.exchange_rates_api)
            response.raise_for_status()
            rates = response.json().get("rates", {})
            return {currency: rates[currency] for currency in self.supported_currencies if currency in rates}
        except requests.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return {}

    def buy_qfc(self, user: str, fiat_amount: float, currency: str) -> bool:
        exchange_rates = self.fetch_exchange_rates()
        if currency not in exchange_rates:
            raise ValueError(f"Unsupported currency: {currency}.")

        if self.compliance:
            if not self.compliance.perform_kyc(user, []):
                raise ValueError("KYC not completed for this user.")
            if not self.compliance.aml_check({"description": f"{fiat_amount} {currency} purchase"}):
                raise ValueError("Transaction flagged by AML check.")

        qfc_amount = fiat_amount / exchange_rates[currency]
        self.record_transaction(user, fiat_amount, currency, qfc_amount)

        self.blockchain.create_user(user)
        entangled_state = self.teleportation.create_entanglement("Onramper", user)
        if not self.teleportation.validate_teleportation(entangled_state):
            raise ValueError("Quantum teleportation of QFC failed.")

        self.blockchain.state_manager.assets["QFC"]["balances"][user] = self.blockchain.state_manager.assets["QFC"]["balances"].get(user, 0) + qfc_amount
        if self.analytics:
            self.analytics.record_transaction_metric(user, fiat_amount, qfc_amount)
        print(f"Successfully purchased {qfc_amount} QFC for {user}.")
        return True

    def record_transaction(self, user: str, fiat_amount: float, currency: str, qfc_amount: float):
        transaction = {
            "user": user,
            "fiat_amount": fiat_amount,
            "currency": currency,
            "qfc_amount": qfc_amount,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.transaction_history.append(transaction)

    def get_transaction_history(self, user: Optional[str] = None) -> List[Dict[str, Any]]:
        if user:
            return [tx for tx in self.transaction_history if tx["user"] == user]
        return self.transaction_history


# -------------------- NFTMarketplace --------------------
class NFTMarketplace:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.nfts: Dict[str, Dict[str, Any]] = {}
        self.teleportation = QuantumTeleportation()

    def teleport_nft(self, token_id: str, sender: str, recipient: str) -> bool:
        nft = self.nfts.get(token_id)
        if not nft or nft["owner"] != sender:
            raise ValueError(f"Sender {sender} does not own NFT {token_id}.")

        entangled_state = self.teleportation.create_entanglement(sender, recipient)
        if not self.teleportation.validate_teleportation(entangled_state):
            raise ValueError(f"Quantum teleportation failed for NFT {token_id}.")

        nft["owner"] = recipient
        print(f"NFT {token_id} teleported from {sender} to {recipient}.")
        return True

    def create_fractional_nft(self, data_id: str, owner: str, metadata: Dict[str, Any], total_units: int):
        if data_id not in self.nfts:
            self.nfts[data_id] = {
                "owner": owner,
                "metadata": metadata,
                "total_units": total_units,
                "available_units": total_units,
                "sale_price": None,
            }
            print(f"Fractional NFT {data_id} created by {owner} with {total_units} units.")


# -------------------- API Routes --------------------
app = Flask(__name__)

@app.route('/nft/teleport', methods=['POST'])
def teleport_nft():
    data = request.json
    try:
        nft_marketplace = NFTMarketplace(blockchain)
        nft_marketplace.teleport_nft(data["token_id"], data["sender"], data["recipient"])
        return jsonify({"success": True, "message": "NFT teleported successfully."})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/onramp/buy', methods=['POST'])
def buy_qfc():
    data = request.json
    try:
        onramper = QFCOnramper(blockchain)
        onramper.buy_qfc(data["user"], data["fiat_amount"], data["currency"])
        return jsonify({"success": True, "message": "Fiat converted to QFC successfully."})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})
