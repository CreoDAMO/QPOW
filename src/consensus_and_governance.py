from typing import Dict
import logging
from src.quantum_wallet import QuantumWallet
from src.state_manager import StateManager
from src.qdpos_manager import QDPoSManager
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


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
    """Hybrid model using QPoS, QDPoS, GPoW, and QPoW."""

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

# Consensus Mechanisms Overview

def consensus_mechanisms_overview():
    """Provides an overview of the consensus mechanisms used in QuantumFuse."""

    mechanisms = {
        "Quantum Proof-of-Work (QPoW)": [
            "QPoW integrates quantum technology to optimize traditional Proof-of-Work mechanisms:",
            "- Quantum Random Number Generators (QRNG):",
            "  Uses quantum randomness to create unpredictable and unforgeable nonces.",
            "  Guarantees fairness and eliminates vulnerabilities associated with pseudo-random number generation.",
            "- Dynamic Difficulty Adjustment:",
            "  Adapts mining difficulty in real-time based on network performance and quantum states.",
            "  Ensures energy efficiency by scaling requirements proportionally to the network load.",
        ],
        "Quantum Proof-of-Stake (QPoS)": [
            "QPoS introduces stake-based consensus to reduce energy consumption while maintaining security:",
            "- Stake-Based Validator Selection:",
            "  Validators are selected proportionally to their QFC holdings.",
            "  Promotes decentralization while ensuring economic commitment.",
            "- Quantum Staking Rewards:",
            "  Stakers earn rewards through quantum teleportation-enhanced distribution mechanisms.",
            "  Includes penalties for malicious behavior, such as double-signing or inactivity.",
        ],
        "Quantum Delegated Proof-of-Stake (QDPoS)": [
            "QDPoS builds on QPoS by introducing delegation and governance:",
            "- Delegation:",
            "  Token holders delegate their stake to trusted validators.",
            "  Increases participation by allowing non-technical users to contribute.",
            "- Governance:",
            "  Validators are elected through a voting system enabled by decentralized identifiers (DIDs).",
            "  Supports on-chain proposals and upgrades for continuous improvement.",
        ],
        "Green Proof-of-Work (GPoW)": [
            "GPoW integrates renewable energy incentives into the mining process:",
            "- Renewable Energy Verification:",
            "  Nodes submit renewable energy certificates for eligibility.",
            "  Ensures that mining operations prioritize sustainability.",
            "- Green Mining Rewards:",
            "  Rewards are dynamically adjusted based on a node’s renewable energy usage ratio.",
            "  Promotes eco-friendly blockchain adoption.",
        ],
    }

    for mechanism, details in mechanisms.items():
        print(mechanism)
        for line in details:
            print("\t" + line)
        print()  # Add a blank line for spacing


# Example call to print consensus mechanisms overview
if __name__ == "__main__":
    consensus_mechanisms_overview()
