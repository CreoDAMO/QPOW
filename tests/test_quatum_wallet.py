import pytest
from src.quantum_wallet import QuantumWallet

@pytest.fixture
def wallet():
    return QuantumWallet("user1", "password")

def test_wallet_creation(wallet):
    assert wallet.user_id == "user1"
    assert wallet.authenticate("password")
    assert not wallet.authenticate("wrong_password")

def test_transaction_signature(wallet):
    tx_data = b"transaction_data"
    signature = wallet.execute_transaction("recipient1", 10.0)["signature"]
    assert wallet.verify_transaction(tx_data, bytes.fromhex(signature), wallet.public_key)

def test_insufficient_balance(wallet):
    with pytest.raises(ValueError):
        wallet.execute_transaction("recipient1", 100.0)
