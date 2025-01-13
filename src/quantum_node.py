# Import BackendSelector for dynamic backend loading
from .backend_selector import BackendSelector
from .pqc_wrapper import PQCWrapper
from .quantum_bridge_wrapper import QuantumBridgeWrapper

# Updated initialization function to integrate with BackendSelector
async def initialize_quantum_node(config_file: str = "config.yaml"):
    selector = BackendSelector(config_file)
    
    # Load backends from configuration
    pqc_backend = selector.get_pqc_backend()
    quantum_backend = selector.get_quantum_backend()
    
    # Initialize wrappers with selected backends
    pqc_wrapper = PQCWrapper(backend=pqc_backend)
    quantum_bridge_wrapper = QuantumBridgeWrapper(backend=quantum_backend)

    # Example of initializing components with these backends
    # TODO: Replace `None` with real network, datastore, and QDPoSManager instances
    network = None  # Load actual network instance
    datastore = None  # Load actual datastore
    qdpos_manager = None  # Load actual QDPoSManager

    app.state.peer_manager = PeerManager(network=network, protocol_host=None)
    app.state.transaction_propagator = TransactionPropagator(gossipsub=None)
    app.state.consensus_manager = ConsensusManager(qdpos_manager=qdpos_manager)
    app.state.node_manager = NodeManager()
    app.state.quantum_storage = QuantumStorage(datastore=datastore)

    logger.info(f"Quantum Node initialized with PQC backend '{pqc_backend}' and Quantum backend '{quantum_backend}'.")

# Main entry point for manual testing or local setup
if __name__ == "__main__":
    import uvicorn
    asyncio.run(initialize_quantum_node())
    uvicorn.run(app, host="0.0.0.0", port=8000)
