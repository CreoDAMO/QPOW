import asyncio
import logging
from typing import Callable, Dict, Any, List
from quantum_lib.teleportation import QuantumTeleportation
from .core import Blockchain, StateManager, Wallet, Transaction
from .onramper import QFCOnramper
from .nft_marketplace import NFTMarketplace
from .optimizer import QuantumAIOptimizer
from .qkd_manager import QKDManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class QuantumServices:
    def __init__(self, blockchain: Blockchain, state_manager: StateManager):
        self.blockchain = blockchain
        self.state_manager = state_manager
        self.teleportation = QuantumTeleportation()
        self.onramper = QFCOnramper(self.blockchain, analytics=None, compliance=None)
        self.nft_marketplace = NFTMarketplace(self.blockchain)
        self.optimizer = QuantumAIOptimizer()
        self.qkd_manager = QKDManager()

    async def process_transactions(self, shard_id: int):
        shard = self.blockchain.shards[shard_id]
        while True:
            pending_transactions = shard.pending_transactions

            if not pending_transactions:
                logger.info(f"No transactions in Shard {shard_id}, waiting...")
                await asyncio.sleep(1)
                continue

            logger.info(f"Processing {len(pending_transactions)} transactions in Shard {shard_id}...")
            tx_details = [
                {
                    "transaction_id": tx.calculate_hash(),
                    "sender": tx.sender,
                    "recipient": tx.recipient,
                    "amount": tx.amount,
                }
                for tx in pending_transactions
            ]
            shard_allocations = self.optimizer.optimize_shard_allocation(tx_details)

            for tx in pending_transactions:
                target_shard_id = shard_allocations[tx.calculate_hash()]
                if shard.shard_id == target_shard_id:
                    self.process_transaction(tx)
                else:
                    logger.info(f"Reassigning transaction {tx.calculate_hash()} to Shard {target_shard_id}.")
                    self.blockchain.shards[target_shard_id].add_transaction(tx)
                    self.optimizer.update_shard_load(target_shard_id, 0.1)

            shard.pending_transactions = []
            self.blockchain.save_state()
            logger.info(f"Transactions in Shard {shard_id} processed and saved.")

    def process_transaction(self, transaction: Transaction):
        sender_wallet = self.state_manager.get_wallet(transaction.sender)
        recipient_wallet = self.state_manager.get_wallet(transaction.recipient)

        if not sender_wallet or not recipient_wallet:
            logger.error(f"Invalid wallets: Sender ({transaction.sender}) or Recipient ({transaction.recipient}).")
            return

        if not sender_wallet.verify_transaction(transaction):
            logger.error(f"Invalid transaction signature for {transaction.calculate_hash()}.")
            return

        if sender_wallet.staked_amount < transaction.amount:
            logger.error(f"Insufficient balance for transaction: {transaction.sender}.")
            return

        # Update balances
        sender_wallet.staked_amount -= transaction.amount
        recipient_wallet.staked_amount += transaction.amount - transaction.fee
        self.state_manager.update_balance(transaction.sender, -transaction.amount)
        self.state_manager.update_balance(transaction.recipient, transaction.amount - transaction.fee)

        # Quantum Key Teleportation
        try:
            self.qkd_manager.teleport_qkd_key(transaction.sender, transaction.recipient)
        except ValueError as e:
            logger.error(f"QKD teleportation failed: {e}")
            return

        logger.info(f"Transaction processed: {transaction.sender} -> {transaction.recipient} ({transaction.amount} QFC).")

    def register_oracle(self, name: str, fetch_data_fn: Callable[[], Dict[str, Any]]):
        self.blockchain.register_oracle(name, fetch_data_fn)
        logger.info(f"Oracle {name} registered successfully.")

    def create_quantum_smart_contract(self, contract_id: str, states: list, creator: str, conditions: Dict[str, Callable]):
        contract = self.blockchain.create_quantum_smart_contract(contract_id, states, creator, conditions)
        logger.info(f"Quantum smart contract {contract_id} created by {creator}.")
        return contract

    def execute_quantum_smart_contract(self, contract_id: str, from_state: str, to_state: str, oracle_name: str):
        contract = self.blockchain.get_quantum_smart_contract(contract_id)
        if not contract:
            logger.error(f"Smart contract {contract_id} not found.")
            return

        contract.transition_state_with_oracle(oracle_name, from_state, to_state)
        logger.info(f"Smart contract {contract_id} transitioned from {from_state} to {to_state} using Oracle {oracle_name}.")

    def create_fractional_nft(self, data_id: str, owner: str, metadata: Dict[str, Any], total_units: int):
        try:
            self.nft_marketplace.create_fractional_nft(data_id, owner, metadata, total_units)
            logger.info(f"Fractional NFT {data_id} created by {owner} with {total_units} units.")
        except ValueError as e:
            logger.error(f"Failed to create fractional NFT {data_id}: {e}.")

    def teleport_nft(self, token_id: str, sender: str, recipient: str):
        try:
            self.nft_marketplace.teleport_nft(token_id, sender, recipient)
            logger.info(f"NFT {token_id} teleported from {sender} to {recipient}.")
        except ValueError as e:
            logger.error(f"Failed to teleport NFT {token_id}: {e}.")

    def generate_teleportation_metrics(self) -> Dict[str, Any]:
        return {
            "qkd_teleportation_success": self.qkd_manager.teleportation.success_count,
            "qkd_teleportation_failures": self.qkd_manager.teleportation.failure_count,
            "shard_utilization": {shard.shard_id: shard.utilization() for shard in self.blockchain.shards},
        }

# Run the transaction processing service
async def run_transaction_processing(services: QuantumServices):
    logger.info("Starting transaction processing for all shards...")
    await asyncio.gather(
        *(services.process_transactions(shard_id) for shard_id in range(len(services.blockchain.shards)))
    )
