# tests/test_blockchain_sharding.py
from core import Blockchain, Transaction

def test_blockchain_initialization():
    blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
    assert len(blockchain.shards) == 3

def test_dynamic_shard_scaling():
    blockchain = Blockchain(num_shards=2, difficulty=4, total_supply=1_000_000)
    assert blockchain.get_shard_utilization() == 0
    blockchain.add_new_shard()
    assert len(blockchain.shards) == 3

def test_shard_to_shard_transaction():
    blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
    tx = Transaction("0xSender1", "0xRecipient1", 50.0)
    assert blockchain.add_transaction(tx) == True
    # Verify the transaction is placed in the correct shard
    shard = blockchain.get_shard_for_address(tx.sender)
    assert len(shard.pending_transactions) == 1
