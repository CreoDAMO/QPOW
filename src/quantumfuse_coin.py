from typing import Dict
import logging

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
