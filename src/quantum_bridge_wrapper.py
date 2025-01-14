class QuantumBridgeWrapper:
    """
    Wrapper for interacting with quantum entanglement backends.
    """

    def __init__(self, backend="quantum_lib"):
        self.backend = backend.lower()
        if self.backend == "quantum_lib":
            import quantum_lib
            self.lib = quantum_lib
        elif self.backend == "qiskit":
            import qiskit
            self.lib = qiskit
        else:
            raise ValueError(
                "Unsupported quantum backend. Choose 'quantum_lib' or 'qiskit'."
            )

    def create_entanglement(self, *args, **kwargs):
        """
        Create an entanglement using the chosen backend.
        """
        return self.lib.create_entanglement(*args, **kwargs)

    def validate_entanglement(self, entanglement_id: str) -> bool:
        """
        Validate an entanglement using the chosen backend.
        """
        return self.lib.validate_entanglement(entanglement_id)
