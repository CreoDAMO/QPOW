from pqcrypto.sign.dilithium2 import verify
from quantum_bridge_wrapper import QuantumBridgeWrapper
from typing import Dict, List, Any, Callable
import time


class QuantumCommunicationContract:
    """
    A contract class for managing quantum communication and AI integration.
    
    This class handles participant registration, key management, and quantum-enhanced
    AI model execution in a secure environment.
    """

    def __init__(
        self, 
        contract_id: str, 
        creator: str, 
        quantum_backend: str = "qiskit"
    ) -> None:
        """
        Initialize the quantum communication contract.

        Args:
            contract_id: Unique identifier for the contract
            creator: Address of the contract creator
            quantum_backend: Name of the quantum computing backend to use
        """
        self.contract_id = contract_id
        self.creator = creator
        self.participants: Dict[str, str] = {}  # {address: did}
        self.ai_models: Dict[str, Callable] = {}  # {model_id: inference_fn}
        self.quantum_bridge = QuantumBridgeWrapper(backend=quantum_backend)
        self.quantum_resource_manager = QuantumResourceManager()
        self.history: List[Dict[str, Any]] = []

    def register_participant(self, participant_address: str, did: str) -> None:
        """
        Register a new participant in the contract.

        Args:
            participant_address: Address of the participant
            did: Decentralized identifier of the participant

        Raises:
            ValueError: If participant is already registered
        """
        if participant_address in self.participants:
            raise ValueError(
                f"Participant {participant_address} already registered."
            )
        self.participants[participant_address] = did

    def register_ai_model(self, model_id: str, inference_fn: Callable) -> None:
        """
        Register an AI model for quantum-enhanced inference.

        Args:
            model_id: Unique identifier for the AI model
            inference_fn: Callable function implementing the model's inference logic

        Raises:
            ValueError: If model_id is already registered
        """
        if model_id in self.ai_models:
            raise ValueError(f"AI model {model_id} already registered.")
        
        self.ai_models[model_id] = inference_fn
        self._log_event("ai_model_registration", {"model_id": model_id})

    def run_quantum_ai_inference(
        self, 
        model_id: str, 
        input_data: Any
    ) -> Any:
        """
        Execute quantum-enhanced AI inference.

        Args:
            model_id: Identifier of the AI model to use
            input_data: Input data for the inference

        Returns:
            The inference results

        Raises:
            ValueError: If the specified model_id is not registered
        """
        if model_id not in self.ai_models:
            raise ValueError(f"AI model {model_id} is not registered.")

        task_id = f"inference-{model_id}"
        
        try:
            self.quantum_resource_manager.allocate_resource(task_id, 10)
            result = self.ai_models[model_id](input_data)
            
            self._log_event(
                "quantum_ai_inference",
                {
                    "model_id": model_id,
                    "input_data": input_data,
                    "result": result
                }
            )
            
            return result
        finally:
            self.quantum_resource_manager.release_resource(task_id)

    def verify_signature(
        self, 
        message: bytes, 
        signature: bytes, 
        public_key: bytes
    ) -> bool:
        """
        Verify a digital signature using post-quantum cryptography.

        Args:
            message: The message that was signed
            signature: The signature to verify
            public_key: The public key to use for verification

        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            return verify(message, signature, public_key)
        except Exception:
            return False

    def get_contract_details(self) -> Dict[str, Any]:
        """
        Get the current state and details of the contract.

        Returns:
            Dict containing contract state information
        """
        return {
            "contract_id": self.contract_id,
            "creator": self.creator,
            "participants": self.participants,
            "ai_models": list(self.ai_models.keys()),
            "history": self.history
        }

    def _log_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Internal method to log contract events with timestamps.

        Args:
            event_type: Type of the event
            event_data: Additional event data
        """
        event_data["event"] = event_type
        event_data["timestamp"] = time.time()
        self.history.append(event_data)
