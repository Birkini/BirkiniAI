import os
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# General configurations for the system
class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENABLE_ENCRYPTION = True

    # Paths for file storage and other directories
    STORAGE_DIR = './storage'
    LOG_DIR = './logs'

    # API key for external data sources
    EXTERNAL_API_KEY = os.environ.get('EXTERNAL_API_KEY', 'apikey')

    # Solana integration setup (example values)
    SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
    SOLANA_PUBLIC_KEY = os.environ.get('SOLANA_PUBLIC_KEY', 'your-solana-public-key')

    @staticmethod
    def init_app(app):
        pass

# Initialize the configurations
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Birkini Core System Setup Complete!")
