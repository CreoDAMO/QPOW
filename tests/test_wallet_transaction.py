# tests/test_wallet_transaction.py
import pytest
from core import Wallet, Transaction

@pytest.fixture
def wallet():
    return Wallet()

def test_wallet_key_generation(wallet):
    assert wallet.private_key is not None
    assert wallet.public_key is not None

def test_transaction_sign_and_verify(wallet):
    tx = Transaction("0x1", "0x2", 100.0)
    tx.sign_transaction(wallet.private_key)
    assert tx.verify_signature(wallet.public_key) == True

def test_failed_transaction_verification(wallet):
    tx = Transaction("0x1", "0x2", 100.0)
    tx.sign_transaction(wallet.private_key)
    # Create a new wallet with different keys to simulate a failed verification
    other_wallet = Wallet()
    assert tx.verify_signature(other_wallet.public_key) == False
