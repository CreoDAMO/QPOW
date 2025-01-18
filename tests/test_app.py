import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/v1/health')
    assert response.status_code == 200
    assert response.json['status'] == "Healthy"


def test_teleport_nft(client):
    response = client.post('/v1/nft/teleport', json={
        "token_id": "nft123",
        "sender": "user_1",
        "recipient": "user_2"
    }, headers={"X-API-KEY": "default-api-key"})
    assert response.status_code == 200
    assert response.json['success'] is True


def test_buy_qfc(client):
    response = client.post('/v1/onramp/buy', json={
        "user": "user_1",
        "fiat_amount": 100,
        "currency": "USD"
    }, headers={"X-API-KEY": "default-api-key"})
    assert response.status_code == 200
    assert response.json['success'] is True


def test_distribute_qkd_key(client):
    response = client.post('/v1/qkd/distribute', json={
        "sender": "user_1",
        "recipient": "user_2"
    }, headers={"X-API-KEY": "default-api-key"})
    assert response.status_code == 200
    assert response.json['success'] is True


def test_teleport_qkd_key(client):
    response = client.post('/v1/qkd/teleport', json={
        "sender": "user_1",
        "recipient": "user_2"
    }, headers={"X-API-KEY": "default-api-key"})
    assert response.status_code == 200
    assert response.json['success'] is True


def test_optimize_shard_allocation(client):
    response = client.post('/v1/shard/optimize', json={
        "transaction_details": []
    }, headers={"X-API-KEY": "default-api-key"})
    assert response.status_code == 200
    assert response.json['success'] is True

# Negative test cases

def test_invalid_route(client):
    response = client.get('/invalid-route')
    assert response.status_code == 404
    assert response.json['success'] is False
    
