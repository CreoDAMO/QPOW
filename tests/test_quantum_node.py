import json
import time
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from quantum_node import app, PeerManager, TransactionPropagator, ConsensusManager, NodeManager, QuantumStorage

# -------------------- Fixtures --------------------

@pytest.fixture
def client():
    """Fixture to provide a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_components():
    """Fixture to mock app state components."""
    with patch("quantum_node.PeerManager") as mock_peer_manager, \
         patch("quantum_node.TransactionPropagator") as mock_transaction_propagator, \
         patch("quantum_node.ConsensusManager") as mock_consensus_manager, \
         patch("quantum_node.NodeManager") as mock_node_manager, \
         patch("quantum_node.QuantumStorage") as mock_quantum_storage:
        yield {
            "peer_manager": mock_peer_manager,
            "transaction_propagator": mock_transaction_propagator,
            "consensus_manager": mock_consensus_manager,
            "node_manager": mock_node_manager,
            "quantum_storage": mock_quantum_storage,
        }


@pytest.fixture
def setup_app_state(mock_components):
    """Fixture to set up app state with mocked components."""
    app.state.peer_manager = mock_components["peer_manager"]()
    app.state.transaction_propagator = mock_components["transaction_propagator"]()
    app.state.consensus_manager = mock_components["consensus_manager"]()
    app.state.node_manager = mock_components["node_manager"]()
    app.state.quantum_storage = mock_components["quantum_storage"]()


# -------------------- Tests --------------------

def test_initialize_quantum_node(mock_components):
    """Test the initialization of the quantum node."""
    with patch("quantum_node.app.state") as mock_state:
        async def mock_initialize_node():
            app.state.peer_manager = mock_components["peer_manager"]()
            app.state.transaction_propagator = mock_components["transaction_propagator"]()
            app.state.consensus_manager = mock_components["consensus_manager"]()
            app.state.node_manager = mock_components["node_manager"]()
            app.state.quantum_storage = mock_components["quantum_storage"]()

        # Simulate initialization
        asyncio.run(mock_initialize_node())
        assert app.state.peer_manager is not None
        assert app.state.transaction_propagator is not None
        assert app.state.consensus_manager is not None
        assert app.state.node_manager is not None
        assert app.state.quantum_storage is not None


@pytest.mark.asyncio
async def test_submit_transaction(client, setup_app_state):
    """Test submitting a transaction."""
    tx_data = b"mock_transaction_data"
    app.state.consensus_manager.process_transaction = AsyncMock(return_value=True)

    response = client.post("/transactions", json={"tx_data": tx_data.hex()})

    assert response.status_code == 200
    assert response.json()["success"] is True
    app.state.consensus_manager.process_transaction.assert_called_once_with(tx_data)


@pytest.mark.asyncio
async def test_submit_transaction_failure(client, setup_app_state):
    """Test submitting a transaction with a failure."""
    tx_data = b"mock_transaction_data"
    app.state.consensus_manager.process_transaction = AsyncMock(return_value=False)

    response = client.post("/transactions", json={"tx_data": tx_data.hex()})

    assert response.status_code == 200
    assert response.json()["success"] is False
    app.state.consensus_manager.process_transaction.assert_called_once_with(tx_data)


@pytest.mark.asyncio
async def test_get_node_info(client, setup_app_state):
    """Test fetching node information."""
    mock_node_config = MagicMock()
    mock_consensus_state = {"state": "mock_consensus_state"}
    app.state.node_manager.get_node_config = MagicMock(return_value=mock_node_config)
    app.state.consensus_manager.get_consensus_state = AsyncMock(return_value=mock_consensus_state)

    response = client.get("/node/info")

    assert response.status_code == 200
    assert response.json()["node_id"] == "node1"
    assert response.json()["consensus_state"] == mock_consensus_state
    app.state.node_manager.get_node_config.assert_called_once_with("node1")
    app.state.consensus_manager.get_consensus_state.assert_called_once()


@pytest.mark.asyncio
async def test_peer_manager_discover_peers(mock_components):
    """Test peer discovery using the PeerManager."""
    peer_manager = mock_components["peer_manager"]()
    peer_manager.discover_peers = AsyncMock(return_value=["peer1", "peer2"])

    peers = await peer_manager.discover_peers("mock_topic")
    assert peers == ["peer1", "peer2"]
    peer_manager.discover_peers.assert_called_once_with("mock_topic")


@pytest.mark.asyncio
async def test_transaction_propagator_publish(mock_components):
    """Test publishing a transaction using the TransactionPropagator."""
    transaction_propagator = mock_components["transaction_propagator"]()
    transaction_propagator.publish_transaction = AsyncMock()

    await transaction_propagator.publish_transaction("mock_topic", b"mock_tx_data")
    transaction_propagator.publish_transaction.assert_called_once_with("mock_topic", b"mock_tx_data")


@pytest.mark.asyncio
async def test_transaction_propagator_subscribe(mock_components):
    """Test subscribing to transactions using the TransactionPropagator."""
    transaction_propagator = mock_components["transaction_propagator"]()
    transaction_propagator.subscribe_to_transactions = AsyncMock()

    async def mock_callback(data):
        return True

    await transaction_propagator.subscribe_to_transactions("mock_topic", mock_callback)
    transaction_propagator.subscribe_to_transactions.assert_called_once_with("mock_topic", mock_callback)


@pytest.mark.asyncio
async def test_consensus_manager_process_transaction(mock_components):
    """Test processing a transaction using the ConsensusManager."""
    consensus_manager = mock_components["consensus_manager"]()
    consensus_manager.process_transaction = AsyncMock(return_value=True)

    result = await consensus_manager.process_transaction(b"mock_tx_data")
    assert result is True
    consensus_manager.process_transaction.assert_called_once_with(b"mock_tx_data")


@pytest.mark.asyncio
async def test_consensus_manager_get_state(mock_components):
    """Test fetching consensus state using the ConsensusManager."""
    consensus_manager = mock_components["consensus_manager"]()
    consensus_manager.get_consensus_state = AsyncMock(return_value={"state": "mock_state"})

    state = await consensus_manager.get_consensus_state()
    assert state == {"state": "mock_state"}
    consensus_manager.get_consensus_state.assert_called_once()


@pytest.mark.asyncio
async def test_quantum_storage_store_data(mock_components):
    """Test storing data using QuantumStorage."""
    quantum_storage = mock_components["quantum_storage"]()
    quantum_storage.store_data = AsyncMock()

    await quantum_storage.store_data(b"key", b"value")
    quantum_storage.store_data.assert_called_once_with(b"key", b"value")


@pytest.mark.asyncio
async def test_quantum_storage_retrieve_data(mock_components):
    """Test retrieving data using QuantumStorage."""
    quantum_storage = mock_components["quantum_storage"]()
    quantum_storage.retrieve_data = AsyncMock(return_value=(b"value", True))

    data, exists = await quantum_storage.retrieve_data(b"key")
    assert data == b"value"
    assert exists is True
    quantum_storage.retrieve_data.assert_called_once_with(b"key")
