import pytest
from src.core import Blockchain, Transaction, Block


@pytest.fixture
def blockchain():
    return Blockchain(
        num_shards=2, difficulty=2, total_supply=1_000_000)

def test_shard_assignment(blockchain):
    tx = Transaction(
        "0xSender", "0xRecipient", 50.0)
    blockchain.assign_transaction_to_shard(tx)
    assert any(
        tx in shard.pending_transactions for shard in blockchain.shards)

def test_mining_difficulty(blockchain):
    block = Block(1, [], "0")
    block.mine_block(
        difficulty=blockchain.difficulty)
    assert block.hash.startswith(
        "0" * blockchain.difficulty)

def test_transaction_validation(blockchain):
    tx = Transaction(
        "0xSender", "0xRecipient", 1000.0)
    assert not blockchain.state_manager.validate_transaction(tx)
    
