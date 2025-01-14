from pqcrypto.sign.dilithium2 import sign, verify
from quantum_bridge_wrapper import QuantumBridgeWrapper
import time
from typing import Dict, List


class QuantumCommunicationContract:
    def __init__(self, contract_id: str, creator: str, quantum_backend: str = "qiskit"):
        self.contract_id = contract_id
        self.creator = creator
        self.participants: Dict[str, str] = {}  # {address: did}
        self.keys: Dict[str, bytes] = {}  # {address: public_key}
        self.entanglements: List[str] = []
        self.quantum_bridge = QuantumBridgeWrapper(backend=quantum_backend)
        self.history: List[Dict[str, any]] = []

    def register_participant(self, participant_address: str, did: str):
        if participant_address in self.participants:
            raise ValueError(f"Participant {participant_address} already registered.")
        self.participants[participant_address] = did

    def generate_key(self, participant_address: str) -> bytes:
        if participant_address in self.keys:
            raise ValueError(f"Key already generated for {participant_address}")
        public_key, _ = self.quantum_bridge.generate_keypair()
        self.keys[participant_address] = public_key
        self.history.append({
            "event": "key_generation",
            "participant": participant_address,
            "timestamp": time.time()
        })
        return public_key

    def distribute_key(self, sender: str, recipient: str):
        if sender not in self.keys or recipient not in self.keys:
            raise ValueError("Both participants must have keys generated.")
        entanglement_id = self.quantum_bridge.create_entanglement(
            self.keys[sender], self.keys[recipient]
        )
        self.entanglements.append(entanglement_id)
        self.history.append({
            "event": "key_distribution",
            "sender": sender,
            "recipient": recipient,
            "timestamp": time.time()
        })
        return f"Key distributed between {sender} 
        and {recipient}"

    def verify_signature(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        try:
            return verify(message, signature, public_key)
        except Exception:
            return False

    def get_contract_details(self) -> Dict[str, any]:
        return {
            "contract_id": self.contract_id,
            "creator": self.creator,
            "participants": self.participants,
            "keys": self.keys,
            "entanglements": self.entanglements,
            "history": self.history
        }
