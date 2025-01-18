import pytest
from src.core import Blockchain, Transaction, Block


@pytest.fixture
def blockchain():
    """Fixture for setting up a blockchain instance."""
    return Blockchain(
        num_shards=2, difficulty=2, total_supply=1_000_000)


def test_shard_assignment(blockchain):
    """Test that a transaction is correctly assigned to a shard."""
    tx = Transaction("0xSender", "0xRecipient", 50.0)
    blockchain.assign_transaction_to_shard(tx)
    assert any(
        tx in shard.pending_transactions for shard in blockchain.shards)


def test_mining_difficulty(blockchain):
    """Test that mining a block meets the required difficulty."""
    block = Block(1, [], "0")
    block.mine_block(
        difficulty=blockchain.difficulty)
    assert block.hash.startswith(
        "0" * blockchain.difficulty)


def test_transaction_validation(blockchain):
    """Test that a transaction is validated based on the state manager's rules."""
    tx = Transaction(
        "0xSender", "0xRecipient", 1000.0)
    assert not blockchain.state_manager.validate_transaction(tx)


def test_block_creation(blockchain):
    """Test block creation with specific attributes."""
    block = Block(2, [Transaction("0xSender", "0xRecipient", 20.0)], "previous_hash")
    assert block.index == 2
    assert len(block.transactions) == 1
    assert block.previous_hash == "previous_hash"


# Additional edge case tests
def test_invalid_transaction_amount(blockchain):
    """Test that a transaction with a negative amount is invalid."""
    tx = Transaction("0xSender", "0xRecipient", -100.0)
    assert not blockchain.state_manager.validate_transaction(tx)


def test_duplicate_transaction(blockchain):
    """Test handling of duplicate transactions within a shard."""
    tx = Transaction("0xSender", "0xRecipient", 25.0)
    blockchain.assign_transaction_to_shard(tx)
    assert any(
        tx in shard.pending_transactions for shard in blockchain.shards)
    blockchain.assign_transaction_to_shard(tx)
    duplicate_count = sum(
        shard.pending_transactions.count(tx) for shard in blockchain.shards
    )
    assert duplicate_count == 1  # Transaction should only appear once


def test_empty_block_hashing(blockchain):
    """Test that an empty block still generates a valid hash."""
    block = Block(3, [], "genesis_hash")
    block.mine_block(difficulty=blockchain.difficulty)
    assert block.hash.startswith("0" * blockchain.difficulty)
