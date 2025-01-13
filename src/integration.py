from src.core import Blockchain, StateManager
from src.quantum_wallet import QuantumWallet
from src.services import QuantumServices
from src.quantum_bridge import QuantumBridge
from src.quantum_smart_contract import QuantumSmartContract
from src.quantum_node import QuantumNode, PeerManager, TransactionPropagator, ConsensusManager, NodeManager, QuantumStorage
from src.quantum_resource_manager import QuantumResourceManager
from src.quantum_secure_manager import QuantumSecureManager
from src.quantum_interface import QuantumInterface, get_quantum_adapter  # Import dynamic adapter logic
from src.backend_selector import BackendSelector  # For backend configuration
from src.app import app

import asyncio
import threading
from hypercorn.asyncio import serve
from hypercorn.config import Config


# -------------------- Initialize Blockchain --------------------
def initialize_blockchain():
    """
    Initialize the core blockchain and state manager.
    """
    blockchain = Blockchain()
    state_manager = StateManager(blockchain)
    return blockchain, state_manager


# -------------------- Initialize Quantum Services --------------------
def initialize_quantum_services(blockchain, state_manager):
    """
    Initialize the Quantum Services module with dependencies.
    """
    quantum_services = QuantumServices(blockchain, state_manager)
    return quantum_services


# -------------------- Initialize Quantum Bridge --------------------
def initialize_quantum_bridge():
    """
    Initialize the Quantum Bridge module for cross-chain interoperability.
    """
    quantum_bridge = QuantumBridge()
    return quantum_bridge


# -------------------- Initialize Quantum Backend --------------------
def initialize_quantum_backend():
    """
    Initialize the quantum backend using QuantumInterface.
    """
    selector = BackendSelector(config_file="config.yaml")
    quantum_backend = selector.get_quantum_backend()
    adapter = get_quantum_adapter(quantum_backend)
    return adapter


# -------------------- Initialize Quantum Smart Contracts --------------------
def initialize_smart_contracts(adapter: QuantumInterface):
    """
    Register and configure quantum smart contracts with dynamic quantum operations.
    """
    smart_contract = QuantumSmartContract(
        contract_id="quantum_contract_1",
        states=["INITIAL", "ACTIVE", "COMPLETED"],
        creator="did:qfc:creator_public_key"
    )
    # Register Oracle
    smart_contract.register_oracle(
        "price_oracle",
        fetch_data_fn=lambda: {"price": 1000}  # Replace with actual oracle logic
    )
    smart_contract.quantum_bridge = adapter  # Use adapter for quantum operations
    return {"quantum_contract_1": smart_contract}


# -------------------- Initialize Quantum Node --------------------
def initialize_quantum_node():
    """
    Initialize the Quantum Node and its sub-components.
    """
    peer_manager = PeerManager()
    transaction_propagator = TransactionPropagator()
    consensus_manager = ConsensusManager()
    node_manager = NodeManager()
    quantum_storage = QuantumStorage()

    quantum_node = QuantumNode(
        peer_manager=peer_manager,
        transaction_propagator=transaction_propagator,
        consensus_manager=consensus_manager,
        node_manager=node_manager,
        storage=quantum_storage
    )
    return quantum_node


# -------------------- Initialize Quantum Resource Manager --------------------
def initialize_quantum_resource_manager():
    """
    Initialize the Quantum Resource Manager.
    """
    quantum_resource_manager = QuantumResourceManager()
    return quantum_resource_manager


# -------------------- Initialize Quantum Secure Manager --------------------
def initialize_quantum_secure_manager():
    """
    Initialize the Quantum Secure Manager.
    """
    quantum_secure_manager = QuantumSecureManager()
    return quantum_secure_manager


# -------------------- Setup Flask App --------------------
def setup_app(blockchain, state_manager, quantum_services, quantum_bridge, smart_contracts, quantum_resource_manager, quantum_secure_manager):
    """
    Set up the Flask app with initialized components.
    """
    app.state.blockchain = blockchain
    app.state.state_manager = state_manager
    app.state.quantum_services = quantum_services
    app.state.quantum_bridge = quantum_bridge
    app.state.smart_contracts = smart_contracts
    app.state.quantum_resource_manager = quantum_resource_manager
    app.state.quantum_secure_manager = quantum_secure_manager


# -------------------- Flask App Runner --------------------
def run_app():
    """
    Run the Flask application using Hypercorn.
    """
    config = Config()
    config.bind = ["0.0.0.0:8000"]  # Update the port as needed
    asyncio.run(serve(app, config))


# -------------------- Quantum Node Runner --------------------
async def run_node(quantum_node: QuantumNode):
    """
    Run the Quantum Node asynchronously.
    """
    await quantum_node.start()


# -------------------- Main Integration --------------------
if __name__ == "__main__":
    # Initialize components
    blockchain, state_manager = initialize_blockchain()
    quantum_services = initialize_quantum_services(blockchain, state_manager)
    quantum_bridge = initialize_quantum_bridge()
    
    quantum_adapter = initialize_quantum_backend()  # Load dynamic backend
    smart_contracts = initialize_smart_contracts(quantum_adapter)
    
    quantum_node = initialize_quantum_node()
    quantum_resource_manager = initialize_quantum_resource_manager()
    quantum_secure_manager = initialize_quantum_secure_manager()

    # Set up the Flask app
    setup_app(blockchain, state_manager, quantum_services, quantum_bridge, smart_contracts, quantum_resource_manager, quantum_secure_manager)

    # Launch Flask app and Quantum Node in parallel
    threading.Thread(target=run_app).start()  # Run Flask app
    asyncio.run(run_node(quantum_node))  # Run Quantum Node
