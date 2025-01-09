from src.core import Blockchain, Transaction

def test_shard_distribution():
    blockchain = Blockchain(num_shards=4, difficulty=4, total_supply=1_000_000)

    # Add transactions
    for i in range(20):
        tx = Transaction(f"0xSender{i}", f"0xRecipient{i}", 50.0)
        blockchain.add_transaction(tx)

    # Ensure transactions are distributed across shards
    shard_counts = [len(shard.pending_transactions) for shard in blockchain.shards]
    assert sum(shard_counts) == 20
    assert max(shard_counts) - min(shard_counts) <= 1  # Ensure balanced distribution
