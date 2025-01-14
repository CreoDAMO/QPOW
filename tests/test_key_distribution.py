import unittest
from src.quantum_secure_manager import QuantumSecureManager


class TestQuantumSecureManager(unittest.TestCase):
    def setUp(self):
        self.manager = QuantumSecureManager()

    def test_key_generation_and_revocation(self):
        public_key = self.manager.generate_key("user123")
        self.assertIn("user123", self.manager.keys)
        self.assertEqual(self.manager.keys["user123"]["public"], public_key)

        # Test revocation
        result = self.manager.revoke_key("user123")
        self.assertEqual(result, "Key revoked for user123")
        self.assertNotIn("user123", self.manager.keys)
