from src.quantum_smart_contract import QuantumSmartContract
from src.quantum_interface import QuantumInterface, get_quantum_adapter
from src.app import app

import asyncio
import threading


# -------------------- Initialize Quantum Backend --------------------
def initialize_quantum_backend():
    """
    Initialize the quantum backend using QuantumInterface.
    """
    from src.config_manager import BackendSelector

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
        creator="did:qfc:creator_public_key",
    )
    # Register Oracle
    smart_contract.register_oracle(
        "price_oracle", fetch_data_fn=lambda: {"price": 1000}  # Example logic
    )
    smart_contract.quantum_bridge = adapter  # Use adapter for quantum operations
    return {"quantum_contract_1": smart_contract}


# -------------------- Setup Flask App --------------------
def setup_app(
    blockchain, state_manager, quantum_services, quantum_bridge, 
    smart_contracts, quantum_resource_manager, quantum_secure_manager
):
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


# -------------------- Main Integration --------------------
def initialize_blockchain():
    """Placeholder for initializing the blockchain."""
    from src.core import Blockchain, StateManager
    blockchain = Blockchain()
    state_manager = StateManager()
    return blockchain, state_manager


def initialize_quantum_services(blockchain, state_manager):
    """Placeholder for initializing quantum services."""
    from src.services import QuantumServices
    return QuantumServices(blockchain, state_manager)


def initialize_quantum_bridge():
    """Placeholder for initializing the quantum bridge."""
    from src.quantum_bridge import QuantumBridge
    return QuantumBridge()


def initialize_quantum_node():
    """Placeholder for initializing the quantum node."""
    from src.quantum_node import QuantumNode
    return QuantumNode()


def initialize_quantum_resource_manager():
    """Placeholder for initializing the quantum resource manager."""
    from src.quantum_resource_manager import QuantumResourceManager
    return QuantumResourceManager()


def initialize_quantum_secure_manager():
    """Placeholder for initializing the quantum secure manager."""
    from src.quantum_secure_manager import QuantumSecureManager
    return QuantumSecureManager()


def run_app():
    """Run the Flask application."""
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:8000"]
    asyncio.run(serve(app, config))


def run_node(node):
    """Run the Quantum Node."""
    node.run()


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
    setup_app(
        blockchain,
        state_manager,
        quantum_services,
        quantum_bridge,
        smart_contracts,
        quantum_resource_manager,
        quantum_secure_manager,
    )

    # Launch Flask app and Quantum Node in parallel
    threading.Thread(target=run_app).start()  # Run Flask app
    asyncio.run(run_node(quantum_node))  # Run Quantum Node
