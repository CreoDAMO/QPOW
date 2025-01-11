import pytest
from src services import QuantumServices
from src core import Blockchain, StateManager, Transaction

@pytest.fixture
def quantum_services():
    blockchain = Blockchain(3, 4, 1_000_000)
    state_manager = StateManager(total_supply=1_000_000)
    return QuantumServices(blockchain, state_manager)

def test_shard_optimization(quantum_services):
    tx = Transaction("0xSender", "0xRecipient", 50.0)
    quantum_services.blockchain.assign_transaction_to_shard(tx)
    assert quantum_services.blockchain.shards[0].utilization() > 0

def test_teleportation_metrics(quantum_services):
    metrics = quantum_services.generate_teleportation_metrics()
    assert "qkd_teleportation_success" in metrics
    assert "qkd_teleportation_failures" in metrics
