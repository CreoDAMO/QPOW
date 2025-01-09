from src.core import StateManager, Wallet

def test_wallet_creation_and_balance():
    state_manager = StateManager(total_supply=1_000_000)
    wallet = state_manager.create_wallet("user1")
    assert wallet is not None
    assert state_manager.wallets["user1"] == wallet

def test_balance_update():
    state_manager = StateManager(total_supply=1_000_000)
    sender = state_manager.create_wallet("user1")
    recipient = state_manager.create_wallet("user2")

    sender_address = sender.get_address()
    recipient_address = recipient.get_address()

    # Initial balances
    state_manager.assets["QFC"]["balances"][sender_address] = 500
    state_manager.assets["QFC"]["balances"][recipient_address] = 0

    # Update balances
    state_manager.assets["QFC"]["balances"][sender_address] -= 100
    state_manager.assets["QFC"]["balances"][recipient_address] += 100

    assert state_manager.assets["QFC"]["balances"][sender_address] == 400
    assert state_manager.assets["QFC"]["balances"][recipient_address] == 100
