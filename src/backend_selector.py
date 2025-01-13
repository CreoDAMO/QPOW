import yaml
import os

class BackendSelector:
    def __init__(self, config_file="config.yaml"):
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file '{config_file}' not found.")

    def get_pqc_backend(self):
        return self.config.get("pqc_backend", "quantcrypt")  # Default to quantcrypt

    def get_quantum_backend(self):
        return self.config.get("quantum_backend", "quantum_lib")  # Default to quantum_lib

# Example usage:
selector = BackendSelector()
pqc_backend = selector.get_pqc_backend()
quantum_backend = selector.get_quantum_backend()

pqc_wrapper = PQCWrapper(backend=pqc_backend)
quantum_bridge_wrapper = QuantumBridgeWrapper(backend=quantum_backend)
