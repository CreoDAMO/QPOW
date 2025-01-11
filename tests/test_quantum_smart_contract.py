import pytest
from unittest.mock import MagicMock, patch
from quantum_smart_contract import QuantumSmartContract


# -------------------- Fixtures --------------------

@pytest.fixture
def quantum_contract():
    """Fixture to provide a QuantumSmartContract instance."""
    contract = QuantumSmartContract(
        contract_id="contract1",
        states=["state1", "state2", "state3"],
        creator="0xCreator"
    )
    return contract


# -------------------- Tests --------------------

# Participant Management
def test_add_participant(quantum_contract):
    quantum_contract.add_participant("0xUser1", "did:example:123")
    assert "0xUser1" in quantum_contract.participants
    assert quantum_contract.did_links["0xUser1"] == "did:example:123"


def test_add_participant_duplicate(quantum_contract):
    quantum_contract.add_participant("0xUser1", "did:example:123")
    with pytest.raises(ValueError, match="Participant 0xUser1 already added."):
        quantum_contract.add_participant("0xUser1", "did:example:123")


# State Management
def test_set_condition(quantum_contract):
    condition_fn = MagicMock(return_value=True)
    quantum_contract.set_condition("state1", "state2", condition_fn)
    assert ("state1", "state2") in quantum_contract.conditions
    assert quantum_contract.conditions[("state1", "state2")] == condition_fn


def test_transition_state_with_oracle_success(quantum_contract):
    condition_fn = MagicMock(return_value=True)
    oracle_fn = MagicMock(return_value={"key": "value"})

    quantum_contract.set_condition("state1", "state2", condition_fn)
    quantum_contract.register_oracle("oracle1", oracle_fn)
    quantum_contract.transition_state_with_oracle("oracle1", "state1", "state2")

    assert quantum_contract.current_state == "state2"
    assert len(quantum_contract.history) == 1
    assert quantum_contract.history[0]["from"] == "state1"
    assert quantum_contract.history[0]["to"] == "state2"


def test_transition_state_with_oracle_failure_condition(quantum_contract):
    condition_fn = MagicMock(return_value=False)
    oracle_fn = MagicMock(return_value={"key": "value"})

    quantum_contract.set_condition("state1", "state2", condition_fn)
    quantum_contract.register_oracle("oracle1", oracle_fn)

    with pytest.raises(ValueError, match="Condition not met for state transition."):
        quantum_contract.transition_state_with_oracle("oracle1", "state1", "state2")

    assert quantum_contract.current_state == "state1"  # State does not change


def test_transition_state_with_oracle_unregistered_oracle(quantum_contract):
    with pytest.raises(ValueError, match="Oracle oracle1 is not registered."):
        quantum_contract.transition_state_with_oracle("oracle1", "state1", "state2")


def test_transition_state_with_oracle_no_condition(quantum_contract):
    oracle_fn = MagicMock(return_value={"key": "value"})
    quantum_contract.register_oracle("oracle1", oracle_fn)

    with pytest.raises(ValueError, match="No condition defined for state transition from state1 to state2."):
        quantum_contract.transition_state_with_oracle("oracle1", "state1", "state2")


# Quantum Entanglement
@patch("quantum_smart_contract.QuantumCircuit")
@patch("quantum_smart_contract.Aer.get_backend")
@patch("quantum_smart_contract.execute")
def test_generate_entanglement(mock_execute, mock_get_backend, mock_quantum_circuit, quantum_contract):
    mock_result = MagicMock()
    mock_result.get_statevector.return_value = [0.707, 0, 0, 0.707]
    mock_execute.return_value.result.return_value = mock_result

    entangled_state = quantum_contract.generate_entanglement()
    assert entangled_state == [0.707, 0, 0, 0.707]


def test_validate_entanglement_success(quantum_contract):
    quantum_contract.entangled_qubits = [0.707, 0, 0, 0.707]
    assert quantum_contract.validate_entanglement()


def test_validate_entanglement_failure(quantum_contract):
    quantum_contract.entangled_qubits = None
    with pytest.raises(ValueError, match="No entangled qubits found. Generate entanglement first."):
        quantum_contract.validate_entanglement()


# Digital Signatures
@patch("quantum_smart_contract.sign")
def test_sign_contract(mock_sign, quantum_contract):
    private_key = b"private_key"
    mock_sign.return_value = b"signature"
    quantum_contract.sign_contract(private_key)

    assert quantum_contract.signature == b"signature"
    mock_sign.assert_called_once()


@patch("quantum_smart_contract.verify")
def test_verify_signature_success(mock_verify, quantum_contract):
    quantum_contract.signature = b"valid_signature"
    public_key = b"public_key"

    mock_verify.return_value = None  # No exception means success
    assert quantum_contract.verify_signature(public_key) is True
    mock_verify.assert_called_once()


@patch("quantum_smart_contract.verify")
def test_verify_signature_failure(mock_verify, quantum_contract):
    quantum_contract.signature = b"invalid_signature"
    public_key = b"public_key"

    mock_verify.side_effect = Exception("Invalid signature")
    with pytest.raises(ValueError, match="Signature verification failed: Invalid signature"):
        quantum_contract.verify_signature(public_key)


# Contract Export and Import
def test_export_contract(quantum_contract):
    quantum_contract.add_participant("0xUser1", "did:example:123")
    contract_json = quantum_contract.export_contract()

    assert isinstance(contract_json, str)
    assert "contract1" in contract_json
    assert "0xUser1" in contract_json


def test_import_contract(quantum_contract):
    contract_json = json.dumps({
        "contract_id": "contract1",
        "state": "state2",
        "participants": ["0xUser1"],
        "history": [{"from": "state1", "to": "state2", "timestamp": time.time()}],
    })

    quantum_contract.import_contract(contract_json)
    assert quantum_contract.contract_id == "contract1"
    assert quantum_contract.current_state == "state2"
    assert "0xUser1" in quantum_contract.participants
    assert len(quantum_contract.history) == 1
