# Import core functionality
from src.core import Blockchain, StateManager, Transaction

# Import services and management
from src.services import QuantumServices
from src.consensus_and_governance import ConsensusManager
from src.quantum_secure_manager import QuantumSecureManager
from src.quantum_resource_manager import QuantumResourceManager

# Import contract-related functionality
from src.quantum_smart_contract import QuantumSmartContract
from src.quantum_communication_contract import QuantumCommunicationContract
from src.quantum_governance_contract import QuantumGovernanceContract
from src.quantum_supplychain_contract import QuantumSupplyChainContract
from src.quantum_ai_integration_contract import QuantumAIIntegrationContract
from src.quantum_random_oracle_contract import QuantumRandomOracleContract
from src.quantum_defi_contract import QuantumDefiContract

# Import quantum infrastructure and environment
from src.quantum_node import QuantumNode, PeerManager, TransactionPropagator
from src.quantum_bridge import QuantumBridge
from src.quantum_interface import QuantumInterface, get_quantum_adapter
from src.fusion_reactor import FusionReactor

# Import utilities and wrappers
from src.quantum_wallet import QuantumWallet
from src.quantum_simulator import QuantumSimulator
from src.quantumfuse_coin import QuantumFuseCoin
from src.backend_selector import BackendSelector
from src.pqc_wrapper import PQCWrapper
from src.quantum_bridge_wrapper import QuantumBridgeWrapper

# Expose key components for simpler imports in external modules
__all__ = [
    "Blockchain",
    "StateManager",
    "Transaction",
    "QuantumServices",
    "ConsensusManager",
    "QuantumSecureManager",
    "QuantumResourceManager",
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
    "QuantumWallet",
    "QuantumBridge",
    "QuantumInterface",
    "get_quantum_adapter",
    "FusionReactor",
    "QuantumSimulator",
    "QuantumFuseCoin",
    "BackendSelector",
    "PQCWrapper",
    "QuantumBridgeWrapper"
]
