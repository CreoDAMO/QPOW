import unittest
from src.quantum_bridge_wrapper import QuantumBridgeWrapper


class TestQuantumBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = QuantumBridgeWrapper(backend="qiskit")

    def test_entanglement(self):
        entanglement_id = self.bridge.create_entanglement()
        self.assertTrue(self.bridge.validate_entanglement(entanglement_id))
