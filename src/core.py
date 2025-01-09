import json
import hashlib
import time
from typing import List, Dict, Optional
from pqcrypto.sign.dilithium2 import generate_keypair, sign, verify
import asyncio

# -------------------- Wallet Class --------------------
class Wallet:
    def __init__(self):
        self.private_key, self.public_key = generate_keypair()

    def get_address(self) -> str:
        """Generate a blockchain address from the public key."""
        return f"0x{self.public_key.hex()}"

    def sign_transaction(self, transaction: "Transaction") -> None:
        """Sign a transaction using the wallet's private key."""
        transaction.sign_transaction(self.private_key)

    def verify_transaction(self, transaction: "Transaction") -> bool:
        """Verify a transaction using the wallet's public key."""
        return transaction.verify_signature(self.public_key)


# -------------------- StateManager Class --------------------
class StateManager:
    """
    Manages the state of QFC assets, balances, and quantum teleportation events across the network.
    """
    def __init__(self, total_supply: int):
        self.assets = {"QFC": {"total_supply": total_supply, "balances": {}}}
        self.wallets: Dict[str, Wallet] = {}
        self.quantum_teleportation_records = {}

    def create_wallet(self, user: str) -> Wallet:
        wallet = Wallet()
        self.wallets[user] = wallet
        return wallet

    def get_wallet(self, user: str) -> Optional[Wallet]:
        return self.wallets.get(user)

    def get_public_key(self, user: str) -> bytes:
        wallet = self.get_wallet(user)
        return wallet.public_key if wallet else b""

    def record_teleportation_event(self, source: str, destination: str):
        """Record a quantum teleportation event."""
        event_id = f"{source}->{destination}"
        self.quantum_teleportation_records[event_id] = time.time()

    def get_teleportation_records(self) -> Dict[str, float]:
        return self.quantum_teleportation_records


# -------------------- Block Class --------------------
class Block:
    def __init__(self, index: int, transactions: List[dict], previous_hash: str, nonce: int = 0, metadata: Optional[dict] = None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = time.time()
        self.metadata = metadata or {}
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_data = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def validate_block(self) -> bool:
        return self.hash == self.calculate_hash()


# -------------------- Transaction Class --------------------
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
        self.signature = sign(tx_hash, private_key)

    def verify_signature(self, public_key: bytes) -> bool:
        tx_hash = self.calculate_hash().encode()
        try:
            verify(tx_hash, self.signature, public_key)
            return True
        except Exception:
            return False


# -------------------- Shard Class --------------------
class Shard:
    def __init__(self, shard_id: int):
        self.shard_id = shard_id
        self.chain = [Block(0, [], "0", metadata={"shard_id": shard_id})]
        self.pending_transactions: List[Transaction] = []

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block):
        self.chain.append(block)

    def validate_shard_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.previous_hash != previous_block.hash or not current_block.validate_block():
                return False
        return True

    async def create_block(self, miner_address: str, state_manager: StateManager) -> Optional[Block]:
        if not self.pending_transactions:
            return None

        metadata = {"miner": miner_address, "shard_id": self.shard_id}
        new_block = Block(
            len(self.chain),
            [tx.to_dict() for tx in self.pending_transactions],
            self.get_latest_block().hash,
            metadata=metadata
        )
        self.pending_transactions = []
        await asyncio.sleep(0)
        return new_block

    def add_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def utilization(self) -> float:
        """Return shard utilization as a ratio."""
        return len(self.pending_transactions) / 100  # Assume 100 as max pending transactions


# -------------------- Blockchain Class --------------------
class Blockchain:
    def __init__(self, num_shards: int, difficulty: int, total_supply: int):
        self.shards = [Shard(i) for i in range(num_shards)]
        self.num_shards = num_shards
        self.difficulty = difficulty
        self.state_manager = StateManager(total_supply)

    def create_user(self, user: str) -> Wallet:
        return self.state_manager.create_wallet(user)

    def get_shard_for_address(self, address: str) -> Shard:
        shard_id = int(address[0], 16) % len(self.shards)
        return self.shards[shard_id]

    def get_shard_utilization(self) -> float:
        """Check average shard utilization."""
        return sum(shard.utilization() for shard in self.shards) / len(self.shards)

    def add_new_shard(self):
        """Dynamically add a new shard when utilization is high."""
        new_shard = Shard(len(self.shards))
        self.shards.append(new_shard)
        self.num_shards += 1
        print(f"New shard added: Shard {new_shard.shard_id}")

    def check_and_scale_shards(self):
        """Monitor and scale shards."""
        if self.get_shard_utilization() > 0.8:
            self.add_new_shard()

    def add_transaction(self, transaction: Transaction) -> bool:
        if self.verify_transaction(transaction):
            shard = self.get_shard_for_address(transaction.sender)
            shard.add_transaction(transaction)
            self.check_and_scale_shards()
            return True
        return False

    def verify_transaction(self, transaction: Transaction) -> bool:
        sender_wallet = self.state_manager.get_wallet(transaction.sender)
        if sender_wallet:
            return transaction.verify_signature(sender_wallet.public_key)
        return False

    async def mine_block(self, miner_address: str) -> Optional[Block]:
        shard = self.get_shard_for_address(miner_address)
        new_block = await shard.create_block(miner_address, self.state_manager)
        if new_block:
            new_block.mine_block(self.difficulty)
            shard.add_block(new_block)
            return new_block
        return None
