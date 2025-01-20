from pqcrypto.sign.dilithium2 import verify
from src.quantum_bridge_wrapper import QuantumBridgeWrapper
from src.quantum_resource_manager import QuantumResourceManager
import time
from typing import Dict, List, Callable, Any


class QuantumAIIntegrationContract:
    def __init__(
        self,
        contract_id: str,
        creator: str,
        quantum_backend: str = "qiskit"
    ) -> None:
        self.contract_id = contract_id
        self.creator = creator
        self.participants: Dict[str, str] = {}
        self.ai_models: Dict[str, Callable] = {}
        self.quantum_bridge = QuantumBridgeWrapper(backend=quantum_backend)
        self.quantum_resource_manager = QuantumResourceManager()
        self.history: List[Dict[str, Any]] = []

    def register_participant(self, participant_address: str, did: str) -> None:
        if participant_address in self.participants:
            raise ValueError(
                f"Participant {participant_address} already registered."
            )
        self.participants[participant_address] = did

    def register_ai_model(self, model_id: str, inference_fn: Callable) -> None:
        if model_id in self.ai_models:
            raise ValueError(f"AI model {model_id} already registered.")
        self.ai_models[model_id] = inference_fn
        self._log_event("ai_model_registration", {"model_id": model_id})

    def run_quantum_ai_inference(
        self,
        model_id: str,
        input_data: Any
    ) -> Any:
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
        try:
            return verify(message, signature, public_key)
        except Exception:
            return False

    def get_contract_details(self) -> Dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "creator": self.creator,
            "participants": self.participants,
            "ai_models": list(self.ai_models.keys()),
            "history": self.history
        }

    def _log_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        event_data["event"] = event_type
        event_data["timestamp"] = time.time()
        self.history.append(event_data)
