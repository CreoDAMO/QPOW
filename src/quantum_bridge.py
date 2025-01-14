import time
from flask import Flask, jsonify, request, abort
from quantum_bridge_wrapper import QuantumBridgeWrapper

# Flask app for API
app = Flask(__name__)

# Instantiate the Quantum Bridge Wrapper
quantum_backend = "qiskit"  # Set the default backend
bridge_wrapper = QuantumBridgeWrapper(backend=quantum_backend)


# -------------------- Hash Time Locked Contract (HTLC) --------------------
class HashTimeLockedContract:
    """
    A Hash Time Locked Contract (HTLC) implementation for secure asset swaps.
    """

    def __init__(self, asset_id: str, hash_preimage: str, timeout: float):
        self.asset_id = asset_id
        self.hash_preimage = hash_preimage
        self.timeout = time.time() + timeout
        self.is_redeemed = False

    def redeem(self, provided_preimage: str) -> bool:
        """
        Redeem the HTLC by providing the correct hash preimage.
        """
        if time.time() > self.timeout:
            raise TimeoutError("HTLC contract expired.")
        if provided_preimage == self.hash_preimage:
            self.is_redeemed = True
            return True
        return False

    def is_expired(self) -> bool:
        """
        Check if the HTLC contract has expired.
        """
        return time.time() > self.timeout


# -------------------- Quantum Bridge --------------------
class QuantumBridge:
    """
    The Quantum Bridge facilitates cross-chain asset transfers and state
    synchronization.
    """

    def __init__(self, quantum_bridge_wrapper: QuantumBridgeWrapper):
        self.entanglements = {}
        self.quantum_bridge_wrapper = quantum_bridge_wrapper

    def create_entanglement(self, chain_a: str, chain_b: str) -> str:
        """
        Create an entanglement between two blockchain networks.
        """
        entanglement_id = self.quantum_bridge_wrapper.create_entanglement()
        self.entanglements[entanglement_id] = {
            "chains": (chain_a, chain_b),
            "created_at": time.time(),
        }
        return entanglement_id

    def validate_entanglement(self, entanglement_id: str) -> bool:
        """
        Validate an entanglement using the quantum bridge wrapper.
        """
        if entanglement_id not in self.entanglements:
            return False
        return self.quantum_bridge_wrapper.validate_entanglement(entanglement_id)

    def list_entanglements(self) -> dict:
        """
        List all active entanglements.
        """
        return self.entanglements


# Instantiate the Quantum Bridge
bridge = QuantumBridge(quantum_bridge_wrapper=bridge_wrapper)


# -------------------- Flask API Endpoints --------------------
@app.route("/bridge/entangle", methods=["POST"])
def create_entanglement():
    """
    API endpoint to create an entanglement between two chains.
    """
    data = request.json
    required_fields = ["chain_a", "chain_b"]

    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")

    entanglement_id = bridge.create_entanglement(
        data["chain_a"],
        data["chain_b"]
    )
    return jsonify({"success": True, "entanglement_id": entanglement_id})


@app.route("/bridge/validate", methods=["POST"])
def validate_entanglement():
    """
    API endpoint to validate an existing entanglement.
    """
    data = request.json
    if "entanglement_id" not in data:
        abort(400, description="Missing required field: entanglement_id")

    entanglement_id = data["entanglement_id"]
    is_valid = bridge.validate_entanglement(entanglement_id)

    if is_valid:
        return jsonify(
            {"success": True, "message": "Entanglement validated successfully."}
        )
    return jsonify(
        {"success": False, "message": "Entanglement validation failed."}
    )


@app.route("/bridge/entanglements", methods=["GET"])
def list_entanglements():
    """
    API endpoint to list all active entanglements.
    """
    entanglements = bridge.list_entanglements()
    return jsonify({"success": True, "entanglements": entanglements})


@app.route("/htlc/redeem", methods=["POST"])
def redeem_htlc():
    """
    API endpoint to redeem an HTLC contract.
    """
    data = request.json
    required_fields = ["asset_id", "provided_preimage"]

    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")

    asset_id = data["asset_id"]
    provided_preimage = data["provided_preimage"]

    htlc_contract = HashTimeLockedContract(
        asset_id, "example_preimage", timeout=300
    )

    try:
        if htlc_contract.redeem(provided_preimage):
            return jsonify(
                {"success": True, "message": "HTLC redeemed successfully."}
            )
        return jsonify({"success": False, "message": "Invalid preimage."})
    except TimeoutError as e:
        app.logger.error(f"TimeoutError: {str(e)}")
        return jsonify(
            {"success": False, "error": "A timeout error has occurred."}
        ), 400


@app.route("/htlc/check", methods=["GET"])
def check_htlc_status():
    """
    API endpoint to check the status of an HTLC contract.
    """
    asset_id = request.args.get("asset_id")
    if not asset_id:
        abort(400, description="Missing required query parameter: asset_id")

    htlc_contract = HashTimeLockedContract(
        asset_id, "example_preimage", timeout=300
    )

    if htlc_contract.is_expired():
        return jsonify({"success": False, "status": "expired"})
    return jsonify({"success": True, "status": "active"})


# -------------------- Error Handlers --------------------
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"success": False, "error": error.description}), 400


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "error": error.description}), 404


# -------------------- Main Function --------------------
if __name__ == "__main__":
    import os

    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1", "t"]
    app.run(debug=debug_mode)
