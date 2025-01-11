import json
import hashlib
import pickle
import time
import uuid
import random
from typing import List, Dict, Optional
from pqcrypto.sign.dilithium2 import generate_keypair, sign, verify
from quantumfuse.modules.qpow import QuantumPoW
import logging
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


# -------------------- Wallet Class --------------------
class Wallet:
    def __init__(self):
        self.private_key, self.public_key = generate_keypair()
        self.did = DID(self.public_key)
        self.staked_amount = 0.0

    def get_address(self) -> str:
        return f"0x{self.public_key.hex()}"

    def sign_transaction(self, transaction: "Transaction") -> None:
        transaction.sign_transaction(self.private_key)

    def verify_transaction(self, transaction: "Transaction") -> bool:
        return transaction.verify_signature(self.public_key)


# -------------------- DID Class --------------------
class DID:
    def __init__(self, public_key: bytes):
        self.identifier = f"did:qfc:{uuid.uuid4()}"
        self.public_key = public_key
        self.services = {}
        self.credentials: Dict[str, str] = {}  # Store verifiable credentials

    def add_service(self, name: str, endpoint: str):
        self.services[name] = endpoint

    def issue_credential(self, action: str, data: str):
        self.credentials[action] = hashlib.sha256(f"{action}:{data}".encode()).hexdigest()

    def verify_credential(self, action: str, credential: str) -> bool:
        return self.credentials.get(action) == credential


# -------------------- StateManager Class --------------------
class StateManager:
    def __init__(self, total_supply: int):
        self.assets = {"QFC": {"total_supply": total_supply, "balances": {}}}
        self.wallets: Dict[str, Wallet] = {}
        self.dids: Dict[str, DID] = {}

    def create_wallet(self, user: str) -> Wallet:
        wallet = Wallet()
        self.wallets[user] = wallet
        self.register_did(wallet)
        return wallet

    def get_wallet(self, user: str) -> Optional[Wallet]:
        return self.wallets.get(user)

    def register_did(self, wallet: Wallet):
        self.dids[wallet.did.identifier] = wallet.did

    def resolve_did(self, identifier: str) -> Optional[DID]:
        return self.dids.get(identifier)

    def reward_miner(self, miner_address: str, reward_amount: float):
        self.assets["QFC"]["balances"].setdefault(miner_address, 0)
        self.assets["QFC"]["balances"][miner_address] += reward_amount
        logger.info(f"Miner {miner_address} rewarded with {reward_amount} QFC.")

    def validate_transaction(self, transaction: "Transaction") -> bool:
        sender_balance = self.assets["QFC"]["balances"].get(transaction.sender, 0)
        if sender_balance < transaction.amount + transaction.fee:
            logger.warning(f"Transaction failed: Insufficient funds for {transaction.sender}.")
            return False
        return True


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
        block_data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        logger.info(f"Block mined: {self.hash}")

    def validate_block(self) -> bool:
        return self.hash == self.calculate_hash()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "hash": self.hash
        }


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
        return hashlib.sha256(tx_data.encode()).hexdigest()

    def sign_transaction(self, private_key: bytes):
        tx_hash = self.calculate_hash().encode()
        self.signature = sign(tx_hash, private_key)

    def verify_signature(self, public_key: bytes) -> bool:
        try:
            tx_hash = self.calculate_hash().encode()
            verify(tx_hash, self.signature, public_key)
            return True
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "asset": self.asset,
            "timestamp": self.timestamp,
            "fee": self.fee,
            "signature": self.signature.hex() if self.signature else None
        }


# -------------------- Shard Class with Load Balancing --------------------
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
        logger.info(f"Transaction added to Shard {self.shard_id}: {transaction.to_dict()}")

    def utilization(self) -> float:
        return len(self.pending_transactions) / 100  # Assume 100 as max pending transactions


# -------------------- Blockchain Class --------------------
class Blockchain:
    def __init__(self, num_shards: int, difficulty: int, total_supply: int, state_file: str = "blockchain_state.pkl"):
        self.shards = [Shard(i) for i in range(num_shards)]
        self.num_shards = num_shards
        self.difficulty = difficulty
        self.state_manager = StateManager(total_supply)
        self.state_file = state_file

    def save_state(self):
        with open(self.state_file, 'wb') as f:
            pickle.dump(self, f)
        logger.info("Blockchain state saved.")

    @staticmethod
    def load_state(state_file: str = "blockchain_state.pkl"):
        try:
            with open(state_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            logger.info("No saved state found, starting a new blockchain.")
            return Blockchain(3, 4, 1_000_000)

    def assign_transaction_to_shard(self, transaction: Transaction):
        least_utilized_shard = min(self.shards, key=lambda shard: shard.utilization())
        least_utilized_shard.add_transaction(transaction)
        logger.info(f"Transaction assigned to Shard {least_utilized_shard.shard_id}")

    async def mine_block(self, miner: Miner) -> Optional[Block]:
        shard = random.choice(self.shards)
        new_block = await shard.create_block(miner.address, self.state_manager)
        if new_block:
            qpow = QuantumPoW(self.difficulty)
            nonce, block_hash = qpow.mine(new_block.to_dict())
            new_block.nonce = nonce
            new_block.hash = block_hash
            shard.add_block(new_block)
            green_reward = miner.calculate_green_reward(50)  # Assume 50 is base reward
            self.state_manager.reward_miner(miner.address, green_reward)
            self.save_state()
            return new_block
        return None
