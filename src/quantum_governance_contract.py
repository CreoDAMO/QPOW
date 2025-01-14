from typing import Dict, Any, Callable
from pqcrypto.sign.dilithium2 import sign, verify
from quantum_random_oracle import QuantumRandomOracleContract
from quantum_secure_manager import QuantumSecureManager
from quantum_resource_manager import QuantumResourceManager
from quantum_simulator import QuantumSimulator
from identity_manager import IdentityManager
from quantum_storage import QuantumStorage
from quantum_services import QuantumServices


class QuantumGovernanceContract:
    def __init__(self, contract_id: str, creator: str):
        self.contract_id = contract_id
        self.creator = creator
        self.authorized_voters: Dict[str, bytes] = {}
        # Mapping of voter addresses to public keys
        self.proposals: Dict[str, Dict[str, Any]] = {}
        # Mapping of proposal IDs to proposal details
        self.votes: Dict[str, Dict[str, bool]] = {}
        # Mapping of proposal IDs to voter addresses and their votes

        self.quantum_random_oracle = QuantumRandomOracleContract(f"{contract_id}_oracle", creator)
        self.quantum_secure_manager = QuantumSecureManager()
        self.quantum_resource_manager = QuantumResourceManager()
        self.quantum_simulator = QuantumSimulator()
        self.identity_manager = IdentityManager()
        self.quantum_storage = QuantumStorage()
        self.quantum_services = QuantumServices()

    def authorize_voter(self, voter_address: str, public_key: bytes):
        """Authorize a voter to participate in the governance process."""
        if voter_address in self.authorized_voters:
            raise ValueError(f"Voter {voter_address} is already authorized.")
        self.authorized_voters[voter_address] = public_key
        self.quantum_random_oracle.authorize_user(voter_address, public_key)

    def create_proposal(
        self, proposer_address: str, title: str, description: str, action: Callable
    ) -> str:
        """Create a new governance proposal."""
        if proposer_address not in self.authorized_voters:
            raise ValueError(f"Proposer {proposer_address} is not authorized.")

        proposal_id = self.quantum_services.generate_proposal_id()
        self.proposals[proposal_id] = {
            "proposer": proposer_address,
            "title": title,
            "description": description,
            "action": action,
            "status": "pending"
        }
        self.votes[proposal_id] = {}
        return proposal_id

    def vote_on_proposal(self, voter_address: str, proposal_id: str, vote: bool):
        """Vote on a governance proposal."""
        if voter_address not in self.authorized_voters:
            raise ValueError(f"Voter {voter_address} is not authorized.")

        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found.")

        self.votes[proposal_id][voter_address] = vote

    def finalize_proposal(self, proposal_id: str):
        """Finalize a governance proposal."""
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found.")

        proposal = self.proposals[proposal_id]
        voters = self.votes[proposal_id]
        total_votes = len(voters)
        positive_votes = sum(1 for vote in voters.values() if vote)

        if positive_votes > total_votes // 2:
            proposal["status"] = "approved"
            proposal["action"]()  # Execute the proposal action
        else:
            proposal["status"] = "rejected"

        self.proposals[proposal_id] = proposal

    def get_contract_details(self) -> Dict[str, Any]:
        """Retrieve the current contract details."""
        return {
            "contract_id": self.contract_id,
            "creator": self.creator,
            "authorized_voters": list(self.authorized_voters.keys()),
            "proposals": self.proposals,
            "votes": self.votes
        }
