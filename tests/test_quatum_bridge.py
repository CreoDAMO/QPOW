import pytest
from src.quantum_bridge import QuantumBridge, HashTimeLockedContract

@pytest.fixture
def bridge():
    return QuantumBridge()

def test_entanglement_creation(bridge):
    entanglement_id = bridge.create_entanglement("chainA", "chainB")
    assert entanglement_id in bridge.entanglements

def test_htlc_redeem():
    htlc = HashTimeLockedContract("asset1", "preimage", timeout=300)
    assert not htlc.redeem("wrong_preimage")
    assert htlc.redeem("preimage")
