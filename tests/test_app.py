import pytest
from unittest.mock import patch
from flask import json
from src.app import app, API_KEY
from src.services import QFCOnramper, NFTMarketplace, QKDManager, QuantumAIOptimizer
from src.core import Blockchain


class TestApp(pytest.TestCase):
    def setUp(self):
        """Set up the Flask test client and necessary mocks."""
        self.app = app.test_client()
        self.blockchain = Blockchain(num_shards=3, difficulty=4, total_supply=1_000_000)
        self.nft_marketplace = NFTMarketplace(self.blockchain)
        self.onramper = QFCOnramper(self.blockchain, analytics=None, compliance=None)
        self.qkd_manager = QKDManager()
        self.quantum_ai_optimizer = QuantumAIOptimizer()

    def test_teleport_nft_success(self):
        """Test successful NFT teleportation."""
        data = {"token_id": "123", "sender": "Alice", "recipient": "Bob"}
        with patch.object(
            self.nft_marketplace, "teleport_nft", return_value=None
        ) as mock_teleport:
            response = self.app.post(
                "/v1/nft/teleport",
                data=json.dumps(data),
                headers={"X-API-KEY": API_KEY},
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json["success"])
            mock_teleport.assert_called_once_with("123", "Alice", "Bob")

    def test_teleport_nft_missing_field(self):
        """Test NFT teleportation fails due to missing recipient field."""
        data = {"token_id": "123", "sender": "Alice"}
        response = self.app.post(
            "/v1/nft/teleport",
            data=json.dumps(data),
            headers={"X-API-KEY": API_KEY},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing required field: recipient")

    def test_teleport_nft_exception(self):
        """Test NFT teleportation fails due to an unexpected exception."""
        data = {"token_id": "123", "sender": "Alice", "recipient": "Bob"}
        with patch.object(
            self.nft_marketplace,
            "teleport_nft", side_effect=ValueError("Unexpected error")
        ):
            response = self.app.post(
                "/v1/nft/teleport",
                data=json.dumps(data),
                headers={"X-API-KEY": API_KEY},
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 400)
            self.assertFalse(response.json["success"])
            self.assertEqual(
                response.json["error"],
                "An error occurred while processing your request.",
            )

    def test_buy_qfc_success(self):
        """Test successful QFC coin purchase."""
        data = {"user": "Alice", "fiat_amount": 100.0, "currency": "USD"}
        with patch.object(self.onramper, "buy_qfc", return_value=None):
            response = self.app.post(
                "/v1/onramp/buy",
                data=json.dumps(data),
                headers={"X-API-KEY": API_KEY},
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json["message"],
                "Fiat converted to QFC coins successfully.",
            )

    def test_optimize_shard_allocation_success(self):
        """Test shard allocation optimization success."""
        data = {
            "transaction_details": [
                {"sender": "Alice", "recipient": "Bob", "amount": 10},
                {"sender": "Bob", "recipient": "Charlie", "amount": 20},
            ]
        }
        mock_result = {0: [0, 1], 1: [2]}
        with patch.object(
            self.quantum_ai_optimizer,
            "optimize_shard_allocation", return_value=mock_result
        ):
            response = self.app.post(
                "/v1/shard/optimize",
                data=json.dumps(data),
                headers={"X-API-KEY": API_KEY},
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["shard_allocations"], mock_result)

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.app.get("/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "Healthy")


if __name__ == "__main__":
    pytest.main()
