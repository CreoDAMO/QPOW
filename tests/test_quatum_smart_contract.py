import pytest
from src.quantum_smart_contract import QuantumSmartContract

@pytest.fixture
def smart_contract():
    return QuantumSmartContract("contract_001", ["draft", "active", "completed"], "creator")

def test_state_transitions(smart_contract):
    smart_contract.set_condition("draft", "active", lambda data: data["approval"] == True)
    assert smart_contract.current_state == "draft"
    smart_contract.transition_state_with_oracle("oracle1", "draft", "active")
    assert smart_contract.current_state == "active"

def test_entanglement_generation(smart_contract):
    entanglement = smart_contract.generate_entanglement()
    assert entanglement is not None
    assert smart_contract.validate_entanglement()
