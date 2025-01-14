from pqcrypto.sign.dilithium2 import sign, verify
from quantum_bridge_wrapper import QuantumBridgeWrapper
import json
import time
from typing import Callable, Dict, List, Any


class QuantumSmartContract:
    """
    Quantum Smart Contract with features for quantum-secured communication,
    resource allocation, and AI-driven decision-making.
    """

    def __init__(
        self, contract_id: str, states: List[str], creator: str,
        quantum_backend: str = "qiskit"
    ):
        self.contract_id = contract_id
        self.states = states
        self.current_state = states[0]
        self.creator = creator
        self.participants: List[str] = []
        self.did_links: Dict[str, str] = {}
        self.conditions: Dict[tuple, Callable] = {}
        self.history: List[Dict[str, Any]] = []
        self.oracles: Dict[str, Callable] = {}
        self.signature = None
        self.quantum_bridge = QuantumBridgeWrapper(backend=quantum_backend)
        self.entangled_qubits = None
        self.resources: Dict[str, Any] = {}

    def add_participant(self, participant_address: str, did: str):
        """Add a participant to the contract with their DID."""
        if participant_address in self.participants:
            raise ValueError(f"Participant {participant_address} already exists.")
        self.participants.append(participant_address)
        self.did_links[participant_address] = did

    def set_condition(self, from_state: str, to_state: str, condition_fn: Callable):
        """Set a condition for transitioning between states."""
        self.conditions[(from_state, to_state)] = condition_fn

    def register_oracle(self, name: str, fetch_data_fn: Callable[[], Any]):
        """Register an oracle to fetch external data."""
        self.oracles[name] = fetch_data_fn

    def transition_state(self, from_state: str, to_state: str, data: Any = None):
        """Transition the contract state, optionally using provided data."""
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
                "data": data  # Include the data used for the transition
            })
        else:
            raise ValueError("Condition not met for state transition.")


    def transition_state_with_oracle(
        self, oracle_name: str, from_state: str, to_state: str
    ):
        """Transition the contract state using oracle data."""
        if oracle_name not in self.oracles:
            raise ValueError(f"Oracle {oracle_name} is not registered.")
        data = self.oracles[oracle_name]()
        self.transition_state(from_state, to_state, data)  # Use the generic transition_state


    def generate_entanglement(self):
        """Generate quantum entanglement using the Quantum Bridge Wrapper."""
        self.entangled_qubits = self.quantum_bridge.create_entanglement()
        return self.entangled_qubits

    def validate_entanglement(self) -> bool:
        """Validate the generated quantum entanglement."""
        if self.entangled_qubits is None:
            raise ValueError("No entangled qubits found. Generate entanglement first.")
        return self.quantum_bridge.validate_entanglement(self.entangled_qubits)

    def sign_contract(self, private_key: bytes):
        """Sign the contract using a private key."""
        data = json.dumps(self.get_contract_details(), sort_keys=True).encode()
        self.signature = sign(data, private_key)

    def verify_signature(self, public_key: bytes) -> bool:
        """Verify the contract's signature using the public key."""
        if not self.signature:
            raise ValueError("No signature found for the contract.")
        data = json.dumps(self.get_contract_details(), sort_keys=True).encode()
        return verify(data, self.signature, public_key)  # Return the verification result


    def allocate_resources(self, task_id: str, resource_type: str, amount: int):
        """Allocate resources like quantum computing or sensor bandwidth."""
        if task_id in self.resources:
            raise ValueError(f"Resources already allocated for task {task_id}.")  # More specific error message
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
        """Retrieve the current contract details."""
        return {
            "contract_id": self.contract_id,
            "state": self.current_state,
            "participants": self.participants,
            "history": self.history,
            "resources": self.resources,
        }

                         
