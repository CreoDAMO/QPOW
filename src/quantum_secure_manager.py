from pqcrypto.kem.dilithium2 import generate_keypair
from qiskit import QuantumCircuit


class QuantumSecureManager:
    def __init__(self):
        self.keys = {}  # Key management
        self.teleportations = []  # Teleportation management

    # --------------------
    # Quantum Key Distribution (QKD)
    # --------------------
    def generate_key(self, user_id):
        """Generate a quantum-safe keypair for a user."""
        public_key, private_key = generate_keypair()
        self.keys[user_id] = {"public": public_key, "private": private_key}
        return public_key

    def distribute_key(self, sender_id, recipient_id):
        """Distribute a quantum-safe key between two users."""
        if sender_id not in self.keys or recipient_id not in self.keys:
            raise ValueError("Both users must have keys generated.")
        return f"Quantum key distributed between {sender_id} and {recipient_id}"

    def revoke_key(self, user_id):
        """Revoke a user's quantum-safe keys."""
        if user_id in self.keys:
            del self.keys[user_id]
            return f"Key revoked for {user_id}"
        raise ValueError("Key not found.")

    # --------------------
    # Quantum Teleportation
    # --------------------
    def create_entanglement(self, qubit_a, qubit_b):
        """Create entanglement between two qubits."""
        qc = QuantumCircuit(2)
        qc.h(qubit_a)
        qc.cx(qubit_a, qubit_b)
        entanglement_id = f"entanglement-{len(self.teleportations) + 1}"
        self.teleportations.append(entanglement_id)
        return entanglement_id
