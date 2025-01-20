from typing import Dict, Any
from pqcrypto.sign.dilithium2 import sign, verify
from src.quantum_resource_manager import QuantumResourceManager
from src.quantum_secure_manager import QuantumSecureManager
from src.quantum_simulator import QuantumSimulator
from identity_manager import IdentityManager
from quantum_storage import QuantumStorage
from src.quantum_services import QuantumServices


class QuantumRandomOracleContract:
    def __init__(self, contract_id: str, creator: str):
        self.contract_id = contract_id
        self.creator = creator
        # Mapping of user addresses to public keys
        self.authorized_users: Dict[str, bytes] = {}
        # Mapping of request IDs to request details
        self.request_history: Dict[str, Dict[str, Any]] = {}
        self.quantum_resource_manager = QuantumResourceManager()
        self.quantum_secure_manager = QuantumSecureManager()
        self.quantum_simulator = QuantumSimulator()
        self.identity_manager = IdentityManager()
        self.quantum_storage = QuantumStorage()
        self.quantum_services = QuantumServices()

    def authorize_user(self, user_address: str, public_key: bytes):
        """Authorize a user to access the Quantum Random Oracle."""
        if user_address in self.authorized_users:
            raise ValueError(f"User {user_address} is already authorized.")
        self.authorized_users[user_address] = public_key

    def generate_random_number(self, user_address: str) -> bytes:
        """Generate a quantum-powered random number."""
        if user_address not in self.authorized_users:
            raise ValueError(
                f"User {user_address} is not authorized to access the Random Oracle."
            )

        # Allocate quantum resources for random number generation
        resource_id = self.quantum_resource_manager.allocate_resources(
            "random_number_generation",
            "quantum_simulator",
            1
        )

        # Generate the random number using the quantum simulator
        random_number = self.quantum_simulator.generate_random_number()

        # Record the request details
        request_id = self.quantum_storage.store_request_details(
            user_address,
            random_number,
            resource_id
        )

        self.request_history[request_id] = {
            "user": user_address,
            "random_number": random_number,
            "resource_id": resource_id,
            "timestamp": self.quantum_storage.get_current_timestamp()
        }

        return random_number

    def verify_random_number(self, request_id: str, signature: bytes) -> bool:
        """Verify the integrity of a random number request."""
        if request_id not in self.request_history:
            raise ValueError(f"Request {request_id} not found in the history.")

        request_details = self.request_history[request_id]
        user_address = request_details["user"]
        public_key = self.authorized_users[user_address]

        # Construct the data to be verified
        data = (
            f"{request_id}:{request_details['random_number']}:"
            f"{request_details['timestamp']}"
        ).encode()

        return verify(data, signature, public_key)

    def sign_random_number_request(self, request_id: str, private_key: bytes) -> bytes:
        """Sign a random number request."""
        if request_id not in self.request_history:
            raise ValueError(f"Request {request_id} not found in the history.")

        request_details = self.request_history[request_id]
        data = (
            f"{request_id}:{request_details['random_number']}:"
            f"{request_details['timestamp']}"
        ).encode()

        return sign(data, private_key)

    def get_contract_details(self) -> Dict[str, Any]:
        """Retrieve the current contract details."""
        return {
            "contract_id": self.contract_id,
            "creator": self.creator,
            "authorized_users": list(self.authorized_users.keys()),
            "request_history": self.request_history
        }
