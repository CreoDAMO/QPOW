import pytest
from unittest.mock import MagicMock, patch
from app import app, API_KEY


# -------------------- Fixtures --------------------

@pytest.fixture
def client():
    """Fixture to provide a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    return app.test_client()


@pytest.fixture
def mock_services():
    """Patch the services used in the app to prevent real operations."""
    with patch("app.nft_marketplace") as mock_nft, \
         patch("app.onramper") as mock_onramper, \
         patch("app.qkd_manager") as mock_qkd, \
         patch("app.quantum_ai_optimizer") as mock_optimizer:
        yield {
            "nft_marketplace": mock_nft,
            "onramper": mock_onramper,
            "qkd_manager": mock_qkd,
            "quantum_ai_optimizer": mock_optimizer,
        }


# -------------------- Tests --------------------

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json["status"] == "Healthy"


def test_unauthorized_request(client):
    """Test that unauthorized requests are blocked."""
    response = client.post("/v1/nft/teleport", json={})
    assert response.status_code == 401
    assert response.json["error"] == "Unauthorized"


def test_teleport_nft_success(client, mock_services):
    """Test teleporting an NFT with valid data."""
    mock_services["nft_marketplace"].teleport_nft.return_value = None
    headers = {"X-API-KEY": API_KEY}
    data = {"token_id": "nft123", "sender": "0xSender", "recipient": "0xRecipient"}

    response = client.post("/v1/nft/teleport", json=data, headers=headers)

    assert response.status_code == 200
    assert response.json["success"] is True
    mock_services["nft_marketplace"].teleport_nft.assert_called_once_with("nft123", "0xSender", "0xRecipient")


def test_teleport_nft_failure(client, mock_services):
    """Test teleporting an NFT with invalid data."""
    mock_services["nft_marketplace"].teleport_nft.side_effect = ValueError("NFT not found")
    headers = {"X-API-KEY": API_KEY}
    data = {"token_id": "invalid", "sender": "0xSender", "recipient": "0xRecipient"}

    response = client.post("/v1/nft/teleport", json=data, headers=headers)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "error" in response.json
    mock_services["nft_marketplace"].teleport_nft.assert_called_once_with("invalid", "0xSender", "0xRecipient")


def test_buy_qfc_success(client, mock_services):
    """Test buying QFC with valid data."""
    mock_services["onramper"].buy_qfc.return_value = None
    headers = {"X-API-KEY": API_KEY}
    data = {"user": "user123", "fiat_amount": 100, "currency": "USD"}

    response = client.post("/v1/onramp/buy", json=data, headers=headers)

    assert response.status_code == 200
    assert response.json["success"] is True
    mock_services["onramper"].buy_qfc.assert_called_once_with("user123", 100, "USD")


def test_buy_qfc_missing_field(client, mock_services):
    """Test buying QFC with missing required fields."""
    headers = {"X-API-KEY": API_KEY}
    data = {"user": "user123", "currency": "USD"}  # Missing fiat_amount

    response = client.post("/v1/onramp/buy", json=data, headers=headers)

    assert response.status_code == 400
    assert "error" in response.json
    mock_services["onramper"].buy_qfc.assert_not_called()


def test_distribute_qkd_key_success(client, mock_services):
    """Test distributing a QKD key with valid data."""
    mock_services["qkd_manager"].distribute_key.return_value = "mock_key"
    headers = {"X-API-KEY": API_KEY}
    data = {"sender": "0xSender", "recipient": "0xRecipient"}

    response = client.post("/v1/qkd/distribute", json=data, headers=headers)

    assert response.status_code == 200
    assert response.json["success"] is True
    assert "mock_key" in response.json["message"]
    mock_services["qkd_manager"].distribute_key.assert_called_once_with("0xSender", "0xRecipient")


def test_distribute_qkd_key_failure(client, mock_services):
    """Test distributing a QKD key with invalid data."""
    mock_services["qkd_manager"].distribute_key.side_effect = ValueError("Invalid sender or recipient")
    headers = {"X-API-KEY": API_KEY}
    data = {"sender": "invalid_sender", "recipient": "0xRecipient"}

    response = client.post("/v1/qkd/distribute", json=data, headers=headers)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "error" in response.json
    mock_services["qkd_manager"].distribute_key.assert_called_once_with("invalid_sender", "0xRecipient")


def test_optimize_shard_allocation_success(client, mock_services):
    """Test optimizing shard allocation with valid transaction details."""
    mock_services["quantum_ai_optimizer"].optimize_shard_allocation.return_value = {"tx1": 0, "tx2": 1}
    headers = {"X-API-KEY": API_KEY}
    data = {"transaction_details": [{"transaction_id": "tx1"}, {"transaction_id": "tx2"}]}

    response = client.post("/v1/shard/optimize", json=data, headers=headers)

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["shard_allocations"] == {"tx1": 0, "tx2": 1}
    mock_services["quantum_ai_optimizer"].optimize_shard_allocation.assert_called_once_with(data["transaction_details"])


def test_optimize_shard_allocation_failure(client, mock_services):
    """Test optimizing shard allocation with invalid transaction details."""
    mock_services["quantum_ai_optimizer"].optimize_shard_allocation.side_effect = ValueError("Invalid transaction details")
    headers = {"X-API-KEY": API_KEY}
    data = {"transaction_details": []}  # Empty list of transactions

    response = client.post("/v1/shard/optimize", json=data, headers=headers)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "error" in response.json
    mock_services["quantum_ai_optimizer"].optimize_shard_allocation.assert_called_once_with(data["transaction_details"])
