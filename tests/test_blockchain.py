from src.core import Blockchain, Transaction

def test_blockchain_initialization():
    blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
    assert len(blockchain.shards) == 3
    assert blockchain.state_manager.assets["QFC"]["total_supply"] == 1_000_000

def test_dynamic_shard_scaling():
    blockchain = Blockchain(num_shards=2, difficulty=4, total_supply=1_000_000)
    assert blockchain.get_shard_utilization() == 0
    blockchain.add_new_shard()
    assert len(blockchain.shards) == 3

def test_shard_to_shard_transaction():
    blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
    sender = blockchain.create_user("user1")
    recipient = blockchain.create_user("user2")
    tx = Transaction(sender.get_address(), recipient.get_address(), 50.0)
    tx.sign_transaction(sender.private_key)
    assert blockchain.add_transaction(tx) is True

    # Verify the transaction is placed in the correct shard
    shard = blockchain.get_shard_for_address(sender.get_address())
    assert len(shard.pending_transactions) == 1
