from qiskit import QuantumCircuit, Aer, execute
from pqcrypto.sign.dilithium2 import sign, verify
import hashlib
import json
import time
from typing import Callable, Dict, List, Any


class QuantumSmartContract:
    """
    Quantum Smart Contract with state management, quantum entanglement generation, and digital signatures.
    """
    def __init__(self, contract_id: str, states: List[str], creator: str):
        self.contract_id = contract_id
        self.states = states
        self.current_state = states[0]
        self.creator = creator
        self.participants: List[str] = []
        self.did_links: Dict[str, str] = {}  # Maps participant addresses to DIDs
        self.conditions: Dict[tuple, Callable] = {}  # State transition conditions
        self.history: List[Dict[str, Any]] = []  # Logs state transitions
        self.oracles: Dict[str, Callable] = {}  # Registered oracles
        self.entangled_qubits = None  # Quantum entanglement representation
        self.signature = None  # Digital signature for contract verification

    # -------------------- Participant Management --------------------

    def add_participant(self, participant_address: str, did: str):
        """Add a participant to the contract with their DID."""
        if participant_address in self.participants:
            raise ValueError(f"Participant {participant_address} already added.")
        self.participants.append(participant_address)
        self.did_links[participant_address] = did

    # -------------------- Condition and Oracle Management --------------------

    def set_condition(self, from_state: str, to_state: str, condition_fn: Callable):
        """Set a condition for transitioning between states."""
        self.conditions[(from_state, to_state)] = condition_fn

    def register_oracle(self, name: str, fetch_data_fn: Callable[[], Any]):
        """Register an oracle to fetch external data."""
        self.oracles[name] = fetch_data_fn

    # -------------------- State Management --------------------

    def transition_state_with_oracle(self, oracle_name: str, from_state: str, to_state: str):
        """Transition the contract state using oracle data."""
        if oracle_name not in self.oracles:
            raise ValueError(f"Oracle {oracle_name} is not registered.")
        
        data = self.oracles[oracle_name]()
        condition_fn = self.conditions.get((from_state, to_state))
        if not condition_fn:
            raise ValueError(f"No condition defined for state transition from {from_state} to {to_state}.")
        
        if condition_fn(data):
            self.current_state = to_state
            self.history.append({"from": from_state, "to": to_state, "timestamp": time.time(), "oracle": oracle_name})
        else:
            raise ValueError("Condition not met for state transition.")

    # -------------------- Quantum Entanglement --------------------

    def generate_entanglement(self):
        """
        Generate quantum entanglement using Qiskit.
        """
        qc = QuantumCircuit(2)
        qc.h(0)  # Apply Hadamard gate to create superposition
        qc.cx(0, 1)  # Apply CNOT gate to entangle qubits
        backend = Aer.get_backend('statevector_simulator')
        result = execute(qc, backend).result()
        self.entangled_qubits = result.get_statevector()
        return self.entangled_qubits

    def validate_entanglement(self) -> bool:
        """Validate the generated quantum entanglement (simplified check)."""
        if self.entangled_qubits is None:
            raise ValueError("No entangled qubits found. Generate entanglement first.")
        return True  # Placeholder for actual validation logic

    # -------------------- Digital Signatures --------------------

    def sign_contract(self, private_key: bytes):
        """Sign the contract using a private key."""
        data = json.dumps(self.get_contract_details(), sort_keys=True).encode()
        self.signature = sign(data, private_key)

    def verify_signature(self, public_key: bytes) -> bool:
        """Verify the contract's signature using the public key."""
        if not self.signature:
            raise ValueError("No signature found for the contract.")
        try:
            data = json.dumps(self.get_contract_details(), sort_keys=True).encode()
            verify(data, self.signature, public_key)
            return True
        except Exception as e:
            raise ValueError(f"Signature verification failed: {str(e)}")

    # -------------------- Contract Details --------------------

    def get_contract_details(self) -> Dict[str, Any]:
        """Retrieve the current contract details."""
        return {
            "contract_id": self.contract_id,
            "state": self.current_state,
            "participants": self.participants,
            "history": self.history,
        }

    def export_contract(self) -> str:
        """Export the contract to JSON for storage or transmission."""
        return json.dumps(self.get_contract_details(), indent=4)

    def import_contract(self, contract_json: str):
        """Import contract details from JSON."""
        details = json.loads(contract_json)
        self.contract_id = details["contract_id"]
        self.current_state = details["state"]
        self.participants = details["participants"]
        self.history = details["history"]
