import unittest
from src.core import Blockchain, StateManager


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.state_manager = StateManager(self.blockchain)
        # Add initial balances
        self.state_manager.update_balance("sender", 100)

    def test_transaction_validation(self):
        transaction = {"sender": "sender", "receiver": "receiver", "amount": 50}
        result = self.state_manager.validate_transaction(transaction)
        self.assertTrue(result)

        # Test insufficient balance
        transaction["amount"] = 200
        result = self.state_manager.validate_transaction(transaction)
        self.assertFalse(result)
