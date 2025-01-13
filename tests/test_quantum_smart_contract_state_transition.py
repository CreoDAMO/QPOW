import unittest
from src.quantum_smart_contract import QuantumSmartContract

class TestQuantumSmartContract(unittest.TestCase):
    def setUp(self):
        self.contract = QuantumSmartContract(
            contract_id="test_contract",
            states=["CREATED", "ACTIVE", "COMPLETED"],
            creator="did:qfc:creator_public_key"
        )
        self.contract.set_condition(
            "CREATED",
            "ACTIVE",
            lambda data: data.get("price") > 500
        )

    def test_state_transition(self):
        # Register an oracle
        self.contract.register_oracle("price_oracle", lambda: {"price": 1000})
        self.contract.transition_state_with_oracle("price_oracle", "CREATED", "ACTIVE")
        self.assertEqual(self.contract.current_state, "ACTIVE")
