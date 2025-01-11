import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.core import Blockchain, StateManager
from src.quantum_wallet import QuantumWallet
from src.services import QuantumServices
from src.quantum_bridge import QuantumBridge
from src.quantum_smart_contract import QuantumSmartContract
from src.quantum_node import QuantumNode, PeerManager, TransactionPropagator, ConsensusManager
from src.app import app

# -------------------- Fixtures --------------------

@pytest.fixture
def mock_blockchain():
    """Mock the Blockchain instance."""
    blockchain = MagicMock(spec=Blockchain)
    blockchain.num_shards = 3
    blockchain.difficulty = 4
    blockchain.total_supply = 1_000_000
    return blockchain


@pytest.fixture
def mock_state_manager():
    """Mock the StateManager instance."""
    state_manager = MagicMock(spec=StateManager)
    state_manager.total_supply = 1_000_000
    return state_manager


@pytest.fixture
def mock_quantum_services(mock_blockchain, mock_state_manager):
    """Mock the QuantumServices instance."""
    return QuantumServices(mock_blockchain, mock_state_manager)


@pytest.fixture
def mock_quantum_bridge():
    """Mock the QuantumBridge instance."""
    return MagicMock(spec=QuantumBridge)


@pytest.fixture
def mock_smart_contract():
    """Mock the QuantumSmartContract instance."""
    contract = QuantumSmartContract(
        contract_id="quantum_contract_1",
        states=["INITIAL", "ACTIVE", "COMPLETED"],
        creator="did:qfc:creator_public_key"
    )
    contract.register_oracle("price_oracle", fetch_data_fn=MagicMock(return_value={"price": 1000}))
    return contract


@pytest.fixture
def mock_peer_manager():
    """Mock the PeerManager instance."""
    return MagicMock(spec=PeerManager)


@pytest.fixture
def mock_transaction_propagator():
    """Mock the TransactionPropagator instance."""
    return MagicMock(spec=TransactionPropagator)


@pytest.fixture
def mock_consensus_manager():
    """Mock the ConsensusManager instance."""
    return MagicMock(spec=ConsensusManager)


@pytest.fixture
def mock_quantum_node(mock_peer_manager, mock_transaction_propagator, mock_consensus_manager):
    """Mock the QuantumNode instance."""
    node = QuantumNode(
        peer_manager=mock_peer_manager,
        transaction_propagator=mock_transaction_propagator,
        consensus_manager=mock_consensus_manager
    )
    node.start_node = AsyncMock()
    return node


@pytest.fixture
def setup_app(mock_blockchain, mock_state_manager, mock_quantum_services, mock_quantum_bridge, mock_smart_contract):
    """Set up the Flask app state."""
    app.state.blockchain = mock_blockchain
    app.state.state_manager = mock_state_manager
    app.state.quantum_services = mock_quantum_services
    app.state.quantum_bridge = mock_quantum_bridge
    app.state.smart_contracts = {"quantum_contract_1": mock_smart_contract}
    return app


# -------------------- Tests --------------------

def test_blockchain_initialization(mock_blockchain):
    """Test the initialization of the blockchain."""
    assert mock_blockchain.num_shards == 3
    assert mock_blockchain.difficulty == 4
    assert mock_blockchain.total_supply == 1_000_000


def test_state_manager_initialization(mock_state_manager):
    """Test the initialization of the state manager."""
    assert mock_state_manager.total_supply == 1_000_000


def test_quantum_services_initialization(mock_quantum_services, mock_blockchain, mock_state_manager):
    """Test the initialization of QuantumServices."""
    assert mock_quantum_services.blockchain == mock_blockchain
    assert mock_quantum_services.state_manager == mock_state_manager


def test_quantum_bridge_initialization(mock_quantum_bridge):
    """Test the initialization of the QuantumBridge."""
    assert isinstance(mock_quantum_bridge, QuantumBridge)


def test_smart_contract_initialization(mock_smart_contract):
    """Test the initialization of a quantum smart contract."""
    assert mock_smart_contract.contract_id == "quantum_contract_1"
    assert mock_smart_contract.states == ["INITIAL", "ACTIVE", "COMPLETED"]
    assert mock_smart_contract.current_state == "INITIAL"
    assert "price_oracle" in mock_smart_contract.oracles


def test_app_state_initialization(setup_app):
    """Test that the Flask app state is correctly initialized."""
    assert app.state.blockchain is not None
    assert app.state.state_manager is not None
    assert app.state.quantum_services is not None
    assert app.state.quantum_bridge is not None
    assert app.state.smart_contracts is not None
    assert "quantum_contract_1" in app.state.smart_contracts


@pytest.mark.asyncio
async def test_quantum_node_start(mock_quantum_node):
    """Test starting the QuantumNode."""
    await mock_quantum_node.start_node()
    mock_quantum_node.start_node.assert_called_once()


@patch("threading.Thread")
@patch("asyncio.run")
def test_parallel_launch(mock_asyncio_run, mock_thread, mock_quantum_node, setup_app):
    """Test parallel launching of the Flask app and QuantumNode."""
    from integration import run_app, run_node

    # Mock the thread and asyncio.run
    mock_thread.return_value.start = MagicMock()

    # Call the functions to test their execution
    run_app()
    asyncio.run(run_node())

    mock_thread.assert_called_once()  # Ensure Flask app starts in a thread
    mock_asyncio_run.assert_called_once_with(mock_quantum_node.start_node())  # Ensure QuantumNode starts


def test_smart_contract_with_oracle(mock_smart_contract):
    """Test a state transition using a smart contract and an oracle."""
    # Simulate a successful oracle condition
    mock_smart_contract.transition_state_with_oracle("price_oracle", "INITIAL", "ACTIVE")
    assert mock_smart_contract.current_state == "ACTIVE"
    assert len(mock_smart_contract.history) == 1
    assert mock_smart_contract.history[0]["from"] == "INITIAL"
    assert mock_smart_contract.history[0]["to"] == "ACTIVE"


@pytest.mark.asyncio
async def test_integration_end_to_end(mock_quantum_node, setup_app):
    """Test an end-to-end integration scenario."""
    # Simulate initializing and starting the QuantumNode
    await mock_quantum_node.start_node()

    # Verify app state is initialized
    assert app.state.blockchain.num_shards == 3
    assert app.state.smart_contracts["quantum_contract_1"].current_state == "INITIAL"

    # Simulate a state transition in the smart contract
    app.state.smart_contracts["quantum_contract_1"].transition_state_with_oracle("price_oracle", "INITIAL", "ACTIVE")
    assert app.state.smart_contracts["quantum_contract_1"].current_state == "ACTIVE"

    # Ensure node start was called
    mock_quantum_node.start_node.assert_called_once()
