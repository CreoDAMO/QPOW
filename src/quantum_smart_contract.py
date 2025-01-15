from pqcrypto.sign.dilithium2 import sign, verify
from quantum_bridge_wrapper import QuantumBridgeWrapper
import json
import time
from typing import Callable, Dict, List, Any


class BaseContract:
    """Base class for all contracts, providing common functionality."""

    def __init__(self, contract_id: str):
        self.contract_id = contract_id
        self.history: List[Dict[str, Any]] = []
        self.signature = None

    def sign_contract(self, private_key: bytes):
        """Signs the contract using a private key."""
        data = json.dumps(self.get_contract_details(), sort_keys=True).encode()
        self.signature = sign(data, private_key)

    def verify_signature(self, public_key: bytes) -> bool:
        """Verifies the contract's signature using the public key."""
        if not self.signature:
            raise ValueError("No signature found for the contract.")
        data = json.dumps(self.get_contract_details(), sort_keys=True).encode()
        return verify(data, self.signature, public_key)

    def get_contract_details(self) -> Dict[str, Any]:
        """Returns the contract details.  Should be overridden by subclasses."""
        return {"contract_id": self.contract_id}


class ResourceAllocationContract(BaseContract):
    """Manages resource allocation."""

    def __init__(self, contract_id: str):
        super().__init__(contract_id)
        self.resources: Dict[str, Any] = {}

    def allocate_resources(self, task_id: str, resource_type: str, amount: int):
        """Allocates resources."""
        if task_id in self.resources:
            raise ValueError(f"Resources already allocated for task {task_id}.")
        self.resources[task_id] = {
            "type": resource_type,
            "amount": amount,
            "timestamp": time.time()
        }
        self.history.append({
            "event": "resource_allocation",
            "task_id": task_id,
            "details": self.resources[task_id]
        })
        return f"Allocated {amount} units of {resource_type} for task {task_id}."

    def get_contract_details(self) -> Dict[str, Any]:
        details = super().get_contract_details()
        details["resources"] = self.resources
        return details


class StateTransitionContract(BaseContract):
    """Handles state transitions based on conditions."""

    def __init__(self, contract_id: str, states: List[str]):
        super().__init__(contract_id)
        self.states = states
        self.current_state = states[0] if states else None
        self.conditions: Dict[tuple, Callable] = {}

    def set_condition(self, from_state: str, to_state: str, condition_fn: Callable):
        """Sets a condition for transitioning between states."""
        self.conditions[(from_state, to_state)] = condition_fn

    def transition_state(self, to_state: str, data: Any = None):
        """Transitions the contract state."""
        from_state = self.current_state
        condition_fn = self.conditions.get((from_state, to_state))
        if not condition_fn:
            raise ValueError(
                f"No condition for transition from {from_state} to {to_state}."
            )
        if condition_fn(data):
            self.current_state = to_state
            self.history.append({
                "from": from_state,
                "to": to_state,
                "timestamp": time.time(),
                "data": data
            })
        else:
            raise ValueError("Condition not met for state transition.")

    def get_contract_details(self) -> Dict[str, Any]:
        details = super().get_contract_details()
        details["state"] = self.current_state
        return details


class QuantumEntanglementContract(BaseContract):
    """Manages quantum entanglement generation and validation."""

    def __init__(self, contract_id: str, quantum_backend: str = "qiskit"):
        super().__init__(contract_id)
        self.quantum_bridge = QuantumBridgeWrapper(backend=quantum_backend)
        self.entangled_qubits = None

    def generate_entanglement(self):
        """Generates quantum entanglement."""
        self.entangled_qubits = self.quantum_bridge.create_entanglement()
        return self.entangled_qubits

    def validate_entanglement(self) -> bool:
        """Validates the generated quantum entanglement."""
        if self.entangled_qubits is None:
            raise ValueError("No entangled qubits found. Generate entanglement first.")
        return self.quantum_bridge.validate_entanglement(self.entangled_qubits)


# Example usage (you can combine these contracts as needed)
resource_contract =ResourceAllocationContract("resource_contract_1")
state_contract =StateTransitionContract("state_contract_1", ["draft", "approved", "executed"])
entanglement_contract =QuantumEntanglementContract("entanglement_contract_1")
