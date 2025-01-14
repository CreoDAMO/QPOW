from typing import Dict
import logging
from src.quantum_wallet import QuantumWallet
from src.state_manager import StateManager
from src.qdpos_manager import QDPoSManager
import random
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# -------------------- Quantum Proof-of-Work (QPOW) --------------------
class QuantumProofOfWork:
    """Quantum Proof-of-Work (QPOW) with quantum randomness and dynamic difficulty."""

    def __init__(self):
        self.mining_rewards = {}

    @staticmethod
    def generate_nonce() -> int:
        """Generate a quantum random nonce."""
        return random.randint(0, 2**32 - 1)  # Replace with QRNG in production

    def validate_nonce(self, block_hash: str, nonce: int, difficulty: int) -> bool:
        """Validate nonce based on difficulty."""
        target = "0" * difficulty
        hash_result = hashlib.sha256(
            f"{block_hash}{nonce}".encode()
        ).hexdigest()
        return hash_result.startswith(target)

    def mine_block(self, block_data: str, difficulty: int) -> Dict:
        """Perform QPOW mining."""
        nonce = self.generate_nonce()
        while not self.validate_nonce(block_data, nonce, difficulty):
            nonce = self.generate_nonce()
        block_hash = hashlib.sha256(
            f"{block_data}{nonce}".encode()
        ).hexdigest()
        logger.info(f"Block mined with nonce {nonce} and hash {block_hash}.")
        return {"hash": block_hash, "nonce": nonce}


# -------------------- Quantum Proof-of-Stake (QPoS) --------------------
class QuantumProofOfStake:
    """Quantum Proof-of-Stake (QPoS) system."""

    def __init__(self):
        self.validators: Dict[str, QuantumWallet] = {}
        self.total_staked = 0

    def register_validator(self, wallet: QuantumWallet, stake: int):
        """Register a validator."""
        wallet.balance -= stake
        self.validators[wallet.get_address()] = wallet
        self.total_staked += stake
        logger.info(
            f"Validator {wallet.get_address()} registered with stake {stake} QFC."
        )

    def select_validator(self) -> QuantumWallet:
        """Select a validator proportional to stake."""
        addresses = list(self.validators.keys())
        stakes = [wallet.balance for wallet in self.validators.values()]
        selected = random.choices(addresses, weights=stakes, k=1)[0]
        logger.info(f"Validator {selected} selected.")
        return self.validators[selected]


# -------------------- Quantum Delegated Proof-of-Stake (QDPoS) --------------------
class QuantumDelegatedProofOfStake:
    """Quantum Delegated Proof-of-Stake (QDPoS) system."""

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.delegates: Dict[str, str] = {}  # Token holders delegating to validators

    def register_delegate(self, holder_address: str, validator_address: str):
        """Register a delegate."""
        self.delegates[holder_address] = validator_address
        logger.info(
            f"Delegate {holder_address} supports validator {validator_address}."
        )

    def validate_block(self, block_data: str) -> bool:
        """Validate a block."""
        validator_address = random.choice(list(self.delegates.values()))
        logger.info(f"Block validated by {validator_address}.")
        return self.state_manager.validate_transaction({"data": block_data})


# -------------------- Green Proof-of-Work (GPoW) --------------------
class GreenProofOfWork:
    """Green Proof-of-Work (GPoW) system incentivizing renewable energy."""

    def __init__(self):
        self.energy_use: Dict[str, float] = {}

    def register_node(self, node_id: str, renewable_ratio: float):
        """Register a node."""
        self.energy_use[node_id] = renewable_ratio
        logger.info(
            f"Node {node_id} registered with renewable ratio {renewable_ratio}."
        )

    def adjust_rewards(self, base_reward: float) -> Dict[str, float]:
        """Adjust rewards based on renewable usage."""
        return {
            node_id: base_reward * (0.5 + 0.5 * ratio)
            for node_id, ratio in self.energy_use.items()
        }


# -------------------- Hybrid Consensus System --------------------
class HybridConsensus:
    """Hybrid model combining QPOW, QPOS, QDPoS, and GPoW."""

    def __init__(self, state_manager: StateManager, qdpos_manager: QDPoSManager):
        self.qpow = QuantumProofOfWork()
        self.qpos = QuantumProofOfStake()
        self.qdpos = QuantumDelegatedProofOfStake(state_manager)
        self.gpow = GreenProofOfWork()
        self.state_manager = state_manager

    def validate_transaction(self, tx_data: Dict) -> bool:
        """Hybrid transaction validation using QPoS and QDPoS."""
        validator = self.qpos.select_validator()
        is_valid = self.state_manager.validate_transaction(tx_data)
        logger.info(
            f"Transaction validated by {validator.get_address()}: "
            f"{'Success' if is_valid else 'Failure'}."
        )
        return is_valid

    def mine_block(
        self, block_data: str, miner_id: str, difficulty: int, reward: float
    ):
        """Mine a block using QPOW and GPoW."""
        mined_block = self.qpow.mine_block(block_data, difficulty)
        rewards = self.gpow.adjust_rewards(reward)
        final_reward = rewards.get(miner_id, 0)
        logger.info(
            f"Block mined: {mined_block['hash']}, reward to {miner_id}: {final_reward}."
        )
