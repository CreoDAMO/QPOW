import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json["status"] == "Healthy"

def test_wallet_creation(client):
    response = client.post("/wallet/create", json={"user_id": "user1", "password": "password"})
    assert response.status_code == 200
    assert response.json["success"]
