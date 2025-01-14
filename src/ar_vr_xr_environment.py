from src.quantum_secure_manager import QuantumSecureManager
from src.analytics_manager import AnalyticsManager
from src.blockchain.blockchain_api import BlockchainAPI
from src.asset_manager import AssetManager
from src.multiplayer_manager import MultiplayerManager
import logging


class ARVREnvironment:
    """
    AR/VR/XR Environment for blockchain and quantum-enhanced applications.
    """

    def __init__(self):
        self.logger = self._setup_logger()
        self.quantum_secure_manager = QuantumSecureManager()
        self.analytics_manager = AnalyticsManager()
        self.blockchain_api = BlockchainAPI()
        self.asset_manager = AssetManager()
        self.multiplayer_manager = MultiplayerManager()

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        return logging.getLogger(__name__)

    def record_interaction_on_blockchain(self, interaction_data):
        """Record user interaction on the blockchain."""
        self.logger.info("Recording interaction on blockchain.")
        self.blockchain_api.record_interaction(interaction_data)

    def secure_communication_with_blockchain(self):
        """Establish secure communication with the blockchain."""
        self.logger.info("Securing communication with blockchain.")
        self.quantum_secure_manager.establish_secure_channel()

    def enable_multiplayer_mode(self):
        """Enable multiplayer mode in the AR/VR environment."""
        self.logger.info("Enabling multiplayer mode.")
        self.multiplayer_manager.initialize()

    def manage_assets(self):
        """Manage assets in the AR/VR environment."""
        self.logger.info("Managing blockchain assets.")
        self.asset_manager.initialize()

    def capture_and_analyze_interaction_data(self):
        """Capture and analyze user interaction data."""
        self.logger.info("Capturing and analyzing interaction data.")
        interaction_data = self.analytics_manager.capture_interaction_data()
        self.analytics_manager.analyze_data(interaction_data)
