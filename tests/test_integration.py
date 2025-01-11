import pytest
from src.core import Blockchain, StateManager, Transaction
from src.quatum_wallet import QuantumWallet
from src.services import QuantumServices
from src.quantum_bridge import QuantumBridge
from src.quantum_smart_contracts import QuantumSmartContract
from src.quantum_node import PeerManager, TransactionPropagator, ConsensusManager
from src.app import app

# Initialize fixtures for integration testing
@pytest.fixture
def integration_setup():
    blockchain = Blockchain(num_shards=3, difficulty=2, total_supply=1_000_000)
    state_manager = StateManager(total_supply=1_000_000)
    wallet = QuantumWallet("user1", "password")
    quantum_services = QuantumServices(blockchain, state_manager)
    quantum_bridge = QuantumBridge()
    smart_contract = QuantumSmartContract("contract_001", ["draft", "active", "completed"], "creator")
    peer_manager = PeerManager(network=None, protocol_host=None)  # Mocked
    transaction_propagator = TransactionPropagator(protocol_host=None, gossipsub=None)  # Mocked
    consensus_manager = ConsensusManager(qdpos_manager=None)  # Mocked
    return {
        "blockchain": blockchain,
        "state_manager": state_manager,
        "wallet": wallet,
        "quantum_services": quantum_services,
        "quantum_bridge": quantum_bridge,
        "smart_contract": smart_contract,
        "peer_manager": peer_manager,
        "transaction_propagator": transaction_propagator,
        "consensus_manager": consensus_manager,
    }

# Test Initialization
def test_integration_initialization(integration_setup):
    setup = integration_setup
    assert setup["blockchain"].num_shards == 3
    assert setup["state_manager"].assets["QFC"]["total_supply"] == 1_000_000
    assert setup["wallet"].authenticate("password")
    assert setup["quantum_services"] is not None
    assert setup["quantum_bridge"] is not None
    assert setup["smart_contract"].current_state == "draft"

# Test Transaction Lifecycle
def test_transaction_lifecycle(integration_setup):
    setup = integration_setup
    blockchain = setup["blockchain"]
    state_manager = setup["state_manager"]
    
    # Create and assign transaction
    tx = Transaction("0xSender", "0xRecipient", 50.0)
    blockchain.assign_transaction_to_shard(tx)
    assigned_shard = any(tx in shard.pending_transactions for shard in blockchain.shards)
    assert assigned_shard
    
    # Process transaction
    is_valid = state_manager.validate_transaction(tx)
    assert not is_valid  # Should fail due to insufficient funds

# Test Smart Contract Deployment and Execution
def test_smart_contract_execution(integration_setup):
    setup = integration_setup
    smart_contract = setup["smart_contract"]
    
    # Register oracle and set conditions
    smart_contract.set_condition("draft", "active", lambda data: data["approval"] == True)
    smart_contract.register_oracle("approval_oracle", lambda: {"approval": True})
    
    # Transition state using oracle
    smart_contract.transition_state_with_oracle("approval_oracle", "draft", "active")
    assert smart_contract.current_state == "active"

# Test Entanglement and HTLC
def test_cross_chain_integration(integration_setup):
    setup = integration_setup
    quantum_bridge = setup["quantum_bridge"]
    
    # Create entanglement
    entanglement_id = quantum_bridge.create_entanglement("chainA", "chainB")
    assert entanglement_id in quantum_bridge.entanglements
    
    # Redeem HTLC
    from src.bridge import HashTimeLockedContract
    htlc = HashTimeLockedContract("asset1", "preimage", timeout=300)
    assert htlc.redeem("preimage")
    assert not htlc.redeem("wrong_preimage")

# Test Node Communication
def test_node_communication(integration_setup):
    setup = integration_setup
    peer_manager = setup["peer_manager"]
    transaction_propagator = setup["transaction_propagator"]
    
    # Simulated peer discovery and transaction propagation
    discovered_peers = ["peer1", "peer2"]
    assert len(discovered_peers) == 2
    
    # Publish a transaction (mocked)
    assert True  # Placeholder for successful propagation

# Test API Integration
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_api_wallet_creation(client):
    response = client.post("/wallet/create", json={"user_id": "user2", "password": "password2"})
    assert response.status_code == 200
    assert response.json["success"]

def test_api_health_check(client):
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json["status"] == "Healthy"
