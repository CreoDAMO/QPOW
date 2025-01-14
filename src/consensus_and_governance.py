from typing import Dict
import logging
from src.quantum_wallet import QuantumWallet
from src.state_manager import StateManager
from src.qdpos_manager import QDPoSManager
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class QuantumFuseCoin:
    """Manage QFC supply and distribution."""

    TOTAL_SUPPLY = 1_000_000_000

    def __init__(self):
        self.allocation = {
            "Founders and Team": {"allocation": 0.15, "vesting_years": 4},
            "Advisors": {"allocation": 0.05, "vesting_years": 2},
            "Private Sale": {"allocation": 0.10},
            "Public Sale": {"allocation": 0.20},
            "Ecosystem Fund": {"allocation": 0.20},
            "Staking Rewards": {"allocation": 0.15},
            "Treasury": {"allocation": 0.15},
        }
        self.allocations = self.allocate_supply()

    def allocate_supply(self) -> Dict[str, int]:
        """Allocate QFC supply."""
        return {
            name: int(self.TOTAL_SUPPLY * details["allocation"])
            for name, details in self.allocation.items()
        }


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
        logger.info(f"Validator {wallet.get_address()} registered with stake {stake}.")

    def select_validator(self) -> QuantumWallet:
        """Select a validator proportional to stake."""
        addresses = list(self.validators.keys())
        stakes = [wallet.balance for wallet in self.validators.values()]
        selected = random.choices(addresses, weights=stakes, k=1)[0]
        logger.info(f"Validator {selected} selected.")
        return self.validators[selected]


class GreenProofOfWork:
    """GPoW system with renewable energy rewards."""

    def __init__(self):
        self.energy_use: Dict[str, float] = {}

    def register_node(self, node_id: str, renewable_ratio: float):
        """Register a node."""
        self.energy_use[node_id] = renewable_ratio
        logger.info(f"Node {node_id} registered with renewable ratio {renewable_ratio}.")

    def adjust_rewards(self, base_reward: float) -> Dict[str, float]:
        """Adjust rewards based on renewable usage."""
        return {
            node_id: base_reward * (0.5 + 0.5 * ratio)
            for node_id, ratio in self.energy_use.items()
        }


class HybridConsensus:
    """Hybrid model using QPoS, QDPoS, and GPoW."""

    def __init__(self, state_manager: StateManager, qdpos_manager: QDPoSManager):
        self.qpos = QuantumProofOfStake()
        self.qdpos_manager = qdpos_manager
        self.gpow = GreenProofOfWork()
        self.state_manager = state_manager

    def validate_transaction(self, tx_data: Dict) -> bool:
        """Hybrid transaction validation."""
        validator = self.qpos.select_validator()
        is_valid = self.state_manager.validate_transaction(tx_data)
        status = "Success" if is_valid else "Failure"
        logger.info(f"Transaction validated by {validator.get_address()}: {status}.")
        return is_valid

    def mine_block(self, miner_id: str, reward: float):
        """Mine a block using GPoW."""
        rewards = self.gpow.adjust_rewards(reward)
        final_reward = rewards.get(miner_id, 0)
        logger.info(f"Block mined by {miner_id}, reward: {final_reward}.")
