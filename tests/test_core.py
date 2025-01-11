import pytest
from unittest.mock import patch, MagicMock
from core import Wallet, StateManager, Transaction, Block, Shard, Blockchain

# ================================
# Wallet Tests
# ================================
def test_wallet_creation():
    wallet = Wallet()
    assert wallet.public_key is not None
    assert wallet.private_key is not None
    assert wallet.get_address().startswith("0x")


@patch("core.sign")
def test_wallet_sign_transaction(mock_sign):
    wallet = Wallet()
    transaction = Transaction(sender=wallet.get_address(), recipient="0xRecipient", amount=100)
    wallet.sign_transaction(transaction)
    mock_sign.assert_called_once()
    assert transaction.signature is not None


@patch("core.verify")
def test_wallet_verify_transaction(mock_verify):
    wallet = Wallet()
    transaction = Transaction(sender=wallet.get_address(), recipient="0xRecipient", amount=100)
    transaction.signature = b"mock_signature"
    mock_verify.return_value = True
    assert wallet.verify_transaction(transaction)
    mock_verify.assert_called_once()


# ================================
# StateManager Tests
# ================================
def test_state_manager_initialization():
    state_manager = StateManager(total_supply=1000)
    assert state_manager.assets["QFC"]["total_supply"] == 1000
    assert state_manager.assets["QFC"]["balances"] == {}


def test_state_manager_update_balance():
    state_manager = StateManager(total_supply=1000)
    address = "0xAddress"
    state_manager.update_balance(address, 100)
    assert state_manager.assets["QFC"]["balances"][address] == 100


def test_state_manager_validate_transaction():
    state_manager = StateManager(total_supply=1000)
    address = "0xAddress"
    state_manager.update_balance(address, 200)
    transaction = Transaction(sender=address, recipient="0xRecipient", amount=100)
    assert state_manager.validate_transaction(transaction)


# ================================
# Transaction Tests
# ================================
def test_transaction_creation():
    transaction = Transaction(sender="0xSender", recipient="0xRecipient", amount=100)
    assert transaction.sender == "0xSender"
    assert transaction.recipient == "0xRecipient"
    assert transaction.amount == 100
    assert transaction.fee == 1.0  # 1% of 100
    assert transaction.signature is None


def test_transaction_hash():
    transaction = Transaction(sender="0xSender", recipient="0xRecipient", amount=100)
    tx_hash = transaction.calculate_hash()
    assert len(tx_hash) == 64  # SHA3-256 hash length in hex


@patch("core.sign")
def test_transaction_sign(mock_sign):
    private_key = b"private_key"
    transaction = Transaction(sender="0xSender", recipient="0xRecipient", amount=100)
    transaction.sign_transaction(private_key)
    mock_sign.assert_called_once()
    assert transaction.signature is not None


@patch("core.verify")
def test_transaction_verify_signature(mock_verify):
    public_key = b"public_key"
    transaction = Transaction(sender="0xSender", recipient="0xRecipient", amount=100)
    transaction.signature = b"mock_signature"
    mock_verify.return_value = True
    assert transaction.verify_signature(public_key)
    mock_verify.assert_called_once()


# ================================
# Block Tests
# ================================
def test_block_creation():
    transactions = [Transaction(sender="0xSender", recipient="0xRecipient", amount=100)]
    block = Block(index=1, transactions=transactions, previous_hash="0xPreviousHash")
    assert block.index == 1
    assert block.transactions == transactions
    assert block.previous_hash == "0xPreviousHash"
    assert block.hash is not None


def test_block_mining():
    transactions = [Transaction(sender="0xSender", recipient="0xRecipient", amount=100)]
    block = Block(index=1, transactions=transactions, previous_hash="0xPreviousHash")
    block.mine_block(difficulty=2)
    assert block.hash.startswith("00")


def test_block_validation():
    transactions = [Transaction(sender="0xSender", recipient="0xRecipient", amount=100)]
    block = Block(index=1, transactions=transactions, previous_hash="0xPreviousHash")
    block.mine_block(difficulty=2)
    assert block.validate_block()


# ================================
# Shard Tests
# ================================
def test_shard_initialization():
    shard = Shard(shard_id=0)
    assert len(shard.chain) == 1  # Genesis block exists
    assert shard.get_latest_block().index == 0
    assert shard.pending_transactions == []


def test_shard_add_block():
    shard = Shard(shard_id=0)
    transactions = [Transaction(sender="0xSender", recipient="0xRecipient", amount=100)]
    block = Block(index=1, transactions=transactions, previous_hash=shard.get_latest_block().hash)
    shard.add_block(block)
    assert len(shard.chain) == 2  # One block added


def test_shard_validate_chain():
    shard = Shard(shard_id=0)
    transactions = [Transaction(sender="0xSender", recipient="0xRecipient", amount=100)]
    block = Block(index=1, transactions=transactions, previous_hash=shard.get_latest_block().hash)
    block.mine_block(difficulty=2)
    shard.add_block(block)
    assert shard.validate_chain()


# ================================
# Blockchain Tests
# ================================
def test_blockchain_initialization():
    blockchain = Blockchain(num_shards=2, difficulty=2, total_supply=1000)
    assert len(blockchain.shards) == 2
    assert blockchain.difficulty == 2
    assert blockchain.state_manager.assets["QFC"]["total_supply"] == 1000


def test_blockchain_assign_transaction_to_shard():
    blockchain = Blockchain(num_shards=2, difficulty=2, total_supply=1000)
    transaction = Transaction(sender="0x1", recipient="0xRecipient", amount=100)
    blockchain.assign_transaction_to_shard(transaction)
    shard_index = int(transaction.sender, 16) % len(blockchain.shards)
    assert transaction in blockchain.shards[shard_index].pending_transactions


@patch("core.Block.mine_block")
def test_blockchain_mine_block(mock_mine_block):
    blockchain = Blockchain(num_shards=2, difficulty=2, total_supply=1000)
    miner = "0xMiner"
    blockchain.shards[0].pending_transactions = [Transaction(sender="0xSender", recipient="0xRecipient", amount=100)]
    mock_mine_block.return_value = None
    blockchain.mine_block(miner)
    assert blockchain.state_manager.assets["QFC"]["balances"][miner] == 50  # Mining reward
