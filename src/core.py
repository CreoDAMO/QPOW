import json
import hashlib
import time
from typing import List, Optional  # Removed unused Dict import
from src.pqc_wrapper import PQCWrapper  # Dynamic cryptography wrapper
from src.backend_selector import BackendSelector  # Dynamic backend selection

# Initialize backend configuration
selector = BackendSelector("config.yaml")
pqc_backend = selector.get_pqc_backend()
pqc_wrapper = PQCWrapper(backend=pqc_backend)


class Wallet:
    def __init__(self):
        self.private_key, self.public_key = pqc_wrapper.generate_keypair()

    def get_address(self) -> str:
        return f"0x{self.public_key.hex()}"

    def sign_transaction(self, transaction: "Transaction") -> None:
        transaction.sign_transaction(self.private_key)

    def verify_transaction(self, transaction: "Transaction") -> bool:
        return transaction.verify_signature(self.public_key)


class StateManager:
    def __init__(self, total_supply: int):
        self.assets = {
            "QFC": {
                "total_supply": total_supply,
                "balances": {},
            }
        }

    def update_balance(self, address: str, amount: float):
        if address not in self.assets["QFC"]["balances"]:
            self.assets["QFC"]["balances"][address] = 0.0
        self.assets["QFC"]["balances"][address] += amount

    def validate_transaction(self, transaction: "Transaction") -> bool:
        sender_balance = self.assets["QFC"]["balances"].get(transaction.sender, 0.0)
        required_balance = transaction.amount + transaction.fee
        return sender_balance >= required_balance


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, asset: str = "QFC"):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.asset = asset
        self.timestamp = time.time()
        self.fee = 0.01 * amount
        self.signature = None

    def calculate_hash(self) -> str:
        tx_data = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha3_256(tx_data.encode()).hexdigest()

    def sign_transaction(self, private_key: bytes):
        tx_hash = self.calculate_hash().encode()
        self.signature = pqc_wrapper.sign(tx_hash, private_key)

    def verify_signature(self, public_key: bytes) -> bool:
        tx_hash = self.calculate_hash().encode()
        try:
            return pqc_wrapper.verify(tx_hash, self.signature, public_key)
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False


class Block:
    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        nonce: int = 0,
    ):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_data = json.dumps(
            {
                "index": self.index,
                "transactions": [tx.calculate_hash() for tx in self.transactions],
                "previous_hash": self.previous_hash,
                "nonce": self.nonce,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        )
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def validate_block(self) -> bool:
        return self.hash == self.calculate_hash()


class Shard:
    def __init__(self, shard_id: int):
        self.shard_id = shard_id
        self.chain = [Block(0, [], "0")]
        self.pending_transactions: List[Transaction] = []

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block):
        self.chain.append(block)

    def validate_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if (
                current_block.previous_hash != previous_block.hash
                or not current_block.validate_block()
            ):
                return False
        return True


class Blockchain:
    def __init__(self, num_shards: int, difficulty: int, total_supply: int):
        self.shards = [Shard(i) for i in range(num_shards)]
        self.difficulty = difficulty
        self.state_manager = StateManager(total_supply)

    def assign_transaction_to_shard(self, transaction: Transaction):
        shard_index = int(transaction.sender, 16) % len(self.shards)
        self.shards[shard_index].pending_transactions.append(transaction)

    async def mine_block(self, miner: str) -> Optional[Block]:
        for shard in self.shards:
            latest_block = shard.get_latest_block()
            new_block = Block(
                len(shard.chain), shard.pending_transactions, latest_block.hash
            )
            new_block.mine_block(self.difficulty)
            shard.add_block(new_block)
            shard.pending_transactions = []
            self.state_manager.update_balance(miner, 50)  # Mining reward
        return new_block
