import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from services import QuantumServices
from core import Blockchain, StateManager, Wallet, Transaction

# ================================
# Fixtures
# ================================

@pytest.fixture
def mock_blockchain():
    blockchain = MagicMock(spec=Blockchain)
    blockchain.shards = [MagicMock(), MagicMock()]  # Mock two shards
    blockchain.save_state = MagicMock()
    return blockchain

@pytest.fixture
def mock_state_manager():
    state_manager = MagicMock(spec=StateManager)
    state_manager.get_wallet = MagicMock()
    return state_manager

@pytest.fixture
def quantum_services(mock_blockchain, mock_state_manager):
    return QuantumServices(blockchain=mock_blockchain, state_manager=mock_state_manager)

@pytest.fixture
def mock_transaction():
    transaction = MagicMock(spec=Transaction)
    transaction.calculate_hash.return_value = "mock_hash"
    transaction.sender = "0xSender"
    transaction.recipient = "0xRecipient"
    transaction.amount = 100
    transaction.fee = 1
    return transaction

# ================================
# Tests for QuantumServices
# ================================

@pytest.mark.asyncio
async def test_process_transactions_no_transactions(quantum_services):
    shard = quantum_services.blockchain.shards[0]
    shard.pending_transactions = []
    shard.shard_id = 0

    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        task = asyncio.create_task(quantum_services.process_transactions(0))
        await asyncio.sleep(0.1)  # Simulate a brief wait
        task.cancel()  # Cancel the infinite loop in the method
        assert shard.pending_transactions == []
        mock_sleep.assert_called()  # Ensure it waits when there are no transactions

@pytest.mark.asyncio
async def test_process_transactions_with_pending_transactions(quantum_services, mock_transaction):
    shard = quantum_services.blockchain.shards[0]
    shard.pending_transactions = [mock_transaction]
    shard.shard_id = 0

    quantum_services.optimizer.optimize_shard_allocation = MagicMock(
        return_value={mock_transaction.calculate_hash(): 0}  # Keep transaction in the same shard
    )
    quantum_services.process_transaction = MagicMock()

    await asyncio.create_task(quantum_services.process_transactions(0))

    # Ensure transaction is processed
    quantum_services.process_transaction.assert_called_once_with(mock_transaction)
    # Ensure shard transactions are cleared
    assert shard.pending_transactions == []

def test_process_transaction_valid(quantum_services, mock_transaction):
    sender_wallet = MagicMock(spec=Wallet)
    recipient_wallet = MagicMock(spec=Wallet)
    sender_wallet.staked_amount = 200

    quantum_services.state_manager.get_wallet.side_effect = lambda address: sender_wallet if address == mock_transaction.sender else recipient_wallet
    sender_wallet.verify_transaction.return_value = True

    quantum_services.process_transaction(mock_transaction)

    # Verify balances updated
    sender_wallet.staked_amount -= mock_transaction.amount
    recipient_wallet.staked_amount += mock_transaction.amount - mock_transaction.fee
    quantum_services.state_manager.update_balance.assert_any_call(mock_transaction.sender, -mock_transaction.amount)
    quantum_services.state_manager.update_balance.assert_any_call(mock_transaction.recipient, mock_transaction.amount - mock_transaction.fee)

def test_process_transaction_invalid_wallets(quantum_services, mock_transaction):
    quantum_services.state_manager.get_wallet.return_value = None  # Simulate invalid wallets

    quantum_services.process_transaction(mock_transaction)

    quantum_services.state_manager.update_balance.assert_not_called()  # Ensure no balance update occurred

def test_process_transaction_invalid_signature(quantum_services, mock_transaction):
    sender_wallet = MagicMock(spec=Wallet)
    recipient_wallet = MagicMock(spec=Wallet)
    sender_wallet.verify_transaction.return_value = False  # Simulate invalid signature

    quantum_services.state_manager.get_wallet.side_effect = lambda address: sender_wallet if address == mock_transaction.sender else recipient_wallet

    quantum_services.process_transaction(mock_transaction)

    quantum_services.state_manager.update_balance.assert_not_called()  # Ensure no balance update occurred

def test_register_oracle(quantum_services):
    fetch_data_fn = MagicMock()
    quantum_services.register_oracle("mock_oracle", fetch_data_fn)

    quantum_services.blockchain.register_oracle.assert_called_once_with("mock_oracle", fetch_data_fn)

def test_create_quantum_smart_contract(quantum_services):
    quantum_services.blockchain.create_quantum_smart_contract = MagicMock(return_value="mock_contract")

    contract = quantum_services.create_quantum_smart_contract(
        contract_id="contract1",
        states=["state1", "state2"],
        creator="0xCreator",
        conditions={"state1_to_state2": MagicMock()},
    )

    assert contract == "mock_contract"
    quantum_services.blockchain.create_quantum_smart_contract.assert_called_once_with(
        "contract1", ["state1", "state2"], "0xCreator", {"state1_to_state2": MagicMock()}
    )

def test_execute_quantum_smart_contract(quantum_services):
    contract = MagicMock()
    quantum_services.blockchain.get_quantum_smart_contract = MagicMock(return_value=contract)

    quantum_services.execute_quantum_smart_contract("contract1", "state1", "state2", "mock_oracle")

    contract.transition_state_with_oracle.assert_called_once_with("mock_oracle", "state1", "state2")

def test_create_fractional_nft(quantum_services):
    quantum_services.nft_marketplace.create_fractional_nft = MagicMock()

    quantum_services.create_fractional_nft(
        data_id="nft1",
        owner="0xOwner",
        metadata={"name": "NFT 1"},
        total_units=10,
    )

    quantum_services.nft_marketplace.create_fractional_nft.assert_called_once_with(
        "nft1", "0xOwner", {"name": "NFT 1"}, 10
    )

def test_teleport_nft(quantum_services):
    quantum_services.nft_marketplace.teleport_nft = MagicMock()

    quantum_services.teleport_nft(token_id="token1", sender="0xSender", recipient="0xRecipient")

    quantum_services.nft_marketplace.teleport_nft.assert_called_once_with("token1", "0xSender", "0xRecipient")

def test_generate_teleportation_metrics(quantum_services):
    quantum_services.qkd_manager.teleportation.success_count = 5
    quantum_services.qkd_manager.teleportation.failure_count = 1
    quantum_services.blockchain.shards = [
        MagicMock(utilization=MagicMock(return_value=0.8)),
        MagicMock(utilization=MagicMock(return_value=0.6)),
    ]

    metrics = quantum_services.generate_teleportation_metrics()

    assert metrics["qkd_teleportation_success"] == 5
    assert metrics["qkd_teleportation_failures"] == 1
    assert metrics["shard_utilization"] == {0: 0.8, 1: 0.6}
