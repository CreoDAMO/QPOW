import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class Transaction:
    """Represents a transaction."""
    
    def __init__(self, sender: str, amount: float, fee: float):
        self.sender = sender
        self.amount = amount
        self.fee = fee


class StateManager:
    """Manages the state of QFC assets and balances."""
    
    def __init__(self, total_supply: int):
        self.assets = {
            "QFC": {
                "total_supply": total_supply,
                "balances": {},
            }
        }

    def update_balance(self, address: str, amount: float):
        """Update the balance for a given address."""
        if address not in self.assets["QFC"]["balances"]:
            self.assets["QFC"]["balances"][address] = 0.0
            logger.info(f"New address added: {address} with initial balance 0.0.")
        
        self.assets["QFC"]["balances"][address] += amount
        logger.info(
        f"Updated balance for {address}: {self.assets['QFC']['balances'][address]}.")

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate a transaction based on the sender's balance."""
        sender_balance = self.assets["QFC"]["balances"].get(transaction.sender, 0.0)
        required_balance = transaction.amount + transaction.fee
        
        if sender_balance < required_balance:
            logger.warning(f"Transaction validation failed for {transaction.sender}: "
                           f"Insufficient balance. Required: {required_balance}, "
                           f"Available: {sender_balance}.")
            return False
        
        logger.info(f"Transaction validated for {transaction.sender}: "
                    f"Amount: {transaction.amount}, Fee: {transaction.fee}.")
        return True

    def get_balance(self, address: str) -> float:
        """Retrieve the balance of the specified address."""
        return self.assets["QFC"]["balances"].get(address, 0.0)                    
