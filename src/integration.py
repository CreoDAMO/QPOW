from src.core import Blockchain, StateManager
from src.wallet import QuantumWallet
from src.services import QuantumServices
from src.bridge import QuantumBridge
from src.smart_contracts import QuantumSmartContract
from src.node import QuantumNode, PeerManager, TransactionPropagator, ConsensusManager
from src.app import app

# Step 1: Initialize Core Blockchain
blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
state_manager = StateManager(total_supply=1_000_000)

# Step 2: Initialize Quantum Services
quantum_services = QuantumServices(blockchain, state_manager)

# Step 3: Initialize Quantum Bridge
quantum_bridge = QuantumBridge()

# Step 4: Register Smart Contracts
smart_contract = QuantumSmartContract(
    contract_id="quantum_contract_1",
    states=["INITIAL", "ACTIVE", "COMPLETED"],
    creator="did:qfc:creator_public_key"
)
smart_contract.register_oracle(
    "price_oracle",
    fetch_data_fn=lambda: {"price": 1000}  # Replace with actual oracle logic
)

# Step 5: Setup App Module
app.state.blockchain = blockchain
app.state.state_manager = state_manager
app.state.quantum_services = quantum_services
app.state.quantum_bridge = quantum_bridge
app.state.smart_contracts = {"quantum_contract_1": smart_contract}

# Step 6: Initialize Quantum Node
peer_manager = PeerManager(network=None, protocol_host=None)  # Replace with actual instances
transaction_propagator = TransactionPropagator(protocol_host=None, gossipsub=None)  # Replace with actual instances
consensus_manager = ConsensusManager(qdpos_manager=None)  # Replace with actual QDPoSManager
quantum_node = QuantumNode(peer_manager, transaction_propagator, consensus_manager)

# Step 7: Launch App and Node
if __name__ == "__main__":
    import asyncio

    # Run Flask app for external APIs
    import threading
    from src.app import app
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    def run_app():
        config = Config()
        config.bind = ["0.0.0.0:8000"]
        asyncio.run(serve(app, config))

    # Start the Quantum Node
    async def run_node():
        await quantum_node.start_node()

    # Launch in parallel
    threading.Thread(target=run_app).start()
    asyncio.run(run_node())
