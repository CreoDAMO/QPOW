import pytest
from unittest.mock import patch, MagicMock
from quantum_wallet import app, QuantumWallet, wallets


# -------------------- Fixtures --------------------

@pytest.fixture
def client():
    """Fixture to provide a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    return app.test_client()


@pytest.fixture
def mock_wallet():
    """Fixture to create a QuantumWallet for testing."""
    wallet = QuantumWallet(user_id="user1", password="password123")
    wallet.balance = 100.0
    wallets["user1"] = wallet
    return wallet


@pytest.fixture
def mock_recipient_wallet():
    """Fixture to create a recipient wallet."""
    wallet = QuantumWallet(user_id="recipient1", password="password123")
    wallet.balance = 50.0
    wallets["recipient1"] = wallet
    return wallet


# -------------------- QuantumWallet Tests --------------------

def test_wallet_creation():
    """Test creating a new QuantumWallet."""
    wallet = QuantumWallet(user_id="user1", password="password123")
    assert wallet.user_id == "user1"
    assert wallet.balance == 0.0
    assert wallet.authenticate("password123") is True
    assert wallet.authenticate("wrong_password") is False


def test_wallet_transaction(mock_wallet, mock_recipient_wallet):
    """Test executing a transaction between wallets."""
    result = mock_wallet.execute_transaction("recipient1", 50.0)

    assert mock_wallet.balance == 50.0
    assert "transaction" in result
    assert "signature" in result


def test_wallet_insufficient_balance(mock_wallet):
    """Test transaction failure due to insufficient balance."""
    with pytest.raises(ValueError, match="Insufficient balance."):
        mock_wallet.execute_transaction("recipient1", 200.0)


@patch("quantum_wallet.messaging.send")
def test_wallet_notify_transaction(mock_messaging, mock_wallet):
    """Test sending a notification for a transaction."""
    mock_messaging.return_value = None
    mock_wallet.notify_transaction("Test notification")
    mock_messaging.assert_called_once()


# -------------------- Flask API Tests --------------------

def test_create_wallet_success(client):
    """Test creating a wallet via the Flask API."""
    response = client.post("/wallet/create", json={"user_id": "new_user", "password": "securepassword"})
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "public_key" in response.json
    assert "new_user" in wallets


def test_create_wallet_duplicate(client, mock_wallet):
    """Test creating a wallet with a duplicate user_id."""
    response = client.post("/wallet/create", json={"user_id": "user1", "password": "securepassword"})
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "error" in response.json


def test_execute_transaction_success(client, mock_wallet, mock_recipient_wallet):
    """Test executing a transaction via the Flask API."""
    response = client.post(
        "/wallet/transaction",
        json={
            "user_id": "user1",
            "password": "password123",
            "recipient": "recipient1",
            "amount": 50.0,
        },
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert wallets["user1"].balance == 50.0
    assert wallets["recipient1"].balance == 100.0


def test_execute_transaction_insufficient_balance(client, mock_wallet, mock_recipient_wallet):
    """Test transaction failure due to insufficient balance."""
    response = client.post(
        "/wallet/transaction",
        json={
            "user_id": "user1",
            "password": "password123",
            "recipient": "recipient1",
            "amount": 200.0,
        },
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "error" in response.json
    assert wallets["user1"].balance == 100.0  # Balance remains unchanged


def test_execute_transaction_invalid_authentication(client, mock_wallet):
    """Test transaction failure due to incorrect authentication."""
    response = client.post(
        "/wallet/transaction",
        json={
            "user_id": "user1",
            "password": "wrong_password",
            "recipient": "recipient1",
            "amount": 50.0,
        },
    )
    assert response.status_code == 401
    assert response.json["success"] is False
    assert "error" in response.json


def test_execute_transaction_invalid_recipient(client, mock_wallet):
    """Test transaction failure due to invalid recipient."""
    response = client.post(
        "/wallet/transaction",
        json={
            "user_id": "user1",
            "password": "password123",
            "recipient": "nonexistent_user",
            "amount": 50.0,
        },
    )
    assert response.status_code == 404
    assert response.json["success"] is False
    assert "error" in response.json


def test_get_wallet_balance_success(client, mock_wallet):
    """Test retrieving a wallet balance."""
    response = client.get("/wallet/balance/user1")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["balance"] == 100.0


def test_get_wallet_balance_invalid_user(client):
    """Test retrieving a balance for a nonexistent wallet."""
    response = client.get("/wallet/balance/nonexistent_user")
    assert response.status_code == 404
    assert response.json["success"] is False
    assert "error" in response.json


# -------------------- Error Handling Tests --------------------

def test_create_wallet_missing_fields(client):
    """Test wallet creation failure due to missing fields."""
    response = client.post("/wallet/create", json={"user_id": "user1"})
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "error" in response.json


def test_execute_transaction_missing_fields(client):
    """Test transaction failure due to missing fields."""
    response = client.post("/wallet/transaction", json={"user_id": "user1", "password": "password123"})
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "error" in response.json
