import unittest
from src.quantum_resource_manager import QuantumResourceManager


class TestQuantumResourceManager(unittest.TestCase):
    def setUp(self):
        self.manager = QuantumResourceManager()

    def test_resource_allocation_and_release(self):
        self.manager.allocate_resource("task1", 5)
        self.assertIn("task1", self.manager.resources)
        self.assertEqual(self.manager.resources["task1"], 5)

        # Test release
        self.manager.release_resource("task1")
        self.assertNotIn("task1", self.manager.resources)
