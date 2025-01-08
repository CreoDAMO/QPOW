# tests/test_state_manager.py
from core import Blockchain, Transaction

def test_wallet_balance_update_after_transaction():
    blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
    sender = blockchain.create_user("user1")
    recipient = blockchain.create_user("user2")
    transaction = Transaction(sender.get_address(), recipient.get_address(), 50.0)
    transaction.sign_transaction(sender.private_key)
    assert blockchain.add_transaction(transaction)
    assert blockchain.state_manager.assets["QFC"]["balances"].get(recipient.get_address()) == 50.0
