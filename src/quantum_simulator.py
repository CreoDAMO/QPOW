from qiskit import QuantumCircuit, Aer, execute
from src.quantum_bridge import QuantumBridgeWrapper
import logging

simulator = Aer.get_backend('qasm_simulator')


class QuantumSimulationManager:
    def __init__(self):
        self.logger = self._setup_logger()
        self.quantum_bridge = QuantumBridgeWrapper(backend="qiskit")

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        return logging.getLogger(__name__)

    def quantum_secure_communication(self):
        """Simulate quantum secure communication using entanglement."""
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure([0, 1], [0, 1])
        result = execute(circuit, simulator, shots=1).result()
        counts = result.get_counts()
        self.logger.info(f"Quantum secure communication simulation result: {counts}")


if __name__ == "__main__":
    qsm = QuantumSimulationManager()
    qsm.quantum_secure_communication()
