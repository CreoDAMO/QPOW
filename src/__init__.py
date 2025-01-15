# src/__init__.py

# Import core functionality
from .core import Blockchain, StateManager, Transaction

# Import services
from .services import QuantumServices

# Import contract-related functionality
from .quantum_smart_contract import QuantumSmartContract
from .quantum_communication_contract import QuantumCommunicationContract
from .quantum_governance_contract import QuantumGovernanceContract
from .quantum_supplychain_contract import QuantumSupplyChainContract
from .quantum_ai_integration_contract import QuantumAIIntegrationContract
from .quantum_random_oracle_contract import QuantumRandomOracleContract
from .quantum_defi_contract import QuantumDefiContract

# Import infrastructure
from .quantum_node import QuantumNode, PeerManager, TransactionPropagator, ConsensusManager

# Import utilities
from .quantum_wallet import QuantumWallet
from .quantum_bridge import QuantumBridge
from .quantum_interface import QuantumInterface, 
get_quantum_adapter

# Expose key components for simpler imports in external modules
__all__ = [
    "Blockchain",
    "StateManager",
    "Transaction",
    "QuantumServices",
    "QuantumSmartContract",
    "QuantumCommunicationContract",
    "QuantumGovernanceContract",
    "QuantumSupplyChainContract",
    "QuantumAIIntegrationContract",
    "QuantumRandomOracleContract",
    "QuantumDefiContract",
    "QuantumNode",
    "PeerManager",
    "TransactionPropagator",
    "ConsensusManager",
    "QuantumWallet",
    "QuantumBridge",
    "QuantumInterface",
    "get_quantum_adapter"
]
