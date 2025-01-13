class QuantumBridgeWrapper:
    def __init__(self, backend="quantum_lib"):
        self.backend = backend.lower()
        if self.backend == "quantum_lib":
            import quantum_lib
            self.lib = quantum_lib
        elif self.backend == "qiskit":
            import qiskit
            self.lib = qiskit
        else:
            raise ValueError("Unsupported quantum backend. Choose 'quantum_lib' or 'qiskit'.")

    def create_entanglement(self, *args, **kwargs):
        return self.lib.create_entanglement(*args, **kwargs)
