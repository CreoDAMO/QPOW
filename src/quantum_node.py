import asyncio
import logging
from .backend_selector import BackendSelector
from .pqc_wrapper import PQCWrapper
from .quantum_bridge_wrapper import QuantumBridgeWrapper
from .peer_manager import PeerManager
from .transaction_propagator import TransactionPropagator
from .consensus_manager import ConsensusManager
from .node_manager import NodeManager
from .quantum_storage import QuantumStorage
from .app import app

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def initialize_quantum_node(config_file: str = "config.yaml"):
    """
    Initialize the Quantum Node with dynamic backends using BackendSelector.
    """
    selector = BackendSelector(config_file)
    pqc_backend = selector.get_pqc_backend()
    quantum_backend = selector.get_quantum_backend()

    # Initialize wrappers
    pqc_wrapper = PQCWrapper(backend=pqc_backend)
    quantum_bridge_wrapper = QuantumBridgeWrapper(backend=quantum_backend)

    # Initialize components
    network, datastore, qdpos_manager = None, None, None
    app.state.peer_manager = PeerManager(network=network, protocol_host=None)
    app.state.transaction_propagator = TransactionPropagator(gossipsub=None)
    app.state.consensus_manager = ConsensusManager(qdpos_manager=qdpos_manager)
    app.state.node_manager = NodeManager()
    app.state.quantum_storage = QuantumStorage(datastore=datastore)

    logger.info(
        f"Quantum Node initialized with PQC backend '{pqc_backend}' "
        f"and Quantum backend '{quantum_backend}'."
    )


if __name__ == "__main__":
    import uvicorn
    asyncio.run(initialize_quantum_node())
    uvicorn.run(app, host="0.0.0.0", port=8000)
