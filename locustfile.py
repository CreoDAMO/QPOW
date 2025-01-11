from locust import HttpUser, TaskSet, task, between

class BlockchainUserBehavior(TaskSet):
    @task
    def submit_transaction(self):
        self.client.post("/v1/transaction/submit", json={
            "sender": "0xCreator123",
            "recipient": "0xRecipient456",
            "amount": 50,
            "asset": "QFC"
        })

    @task
    def query_balance(self):
        self.client.get("/v1/wallet/balance?wallet_id=0xCreator123")

class QuantumFuseUser(HttpUser):
    tasks = [BlockchainUserBehavior]
    wait_time = between(1, 5)
