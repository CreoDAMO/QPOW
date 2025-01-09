# tests/test_stress_transaction.py
import time
from src.core import Blockchain, Transaction

def test_transaction_throughput():
    blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
    start_time = time.time()

    for i in range(1000):
        tx = Transaction(f"user_{i}", f"user_{i+1}", 10.0)
        blockchain.add_transaction(tx)

    end_time = time.time()
    print(f"Processed 1000 transactions in {end_time - start_time:.2f} seconds")
