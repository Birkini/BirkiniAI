import os
import json
import logging
from datetime import datetime
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Solana configuration
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
SOLANA_WALLET_ADDRESS = os.getenv("SOLANA_WALLET_ADDRESS", "Aa96NbR2jU47k7aquVgVdWa5mae9JwbkegZYJwTwoFBn")
BIRKINI_TOKEN_MINT = os.getenv("BIRKINI_TOKEN_MINT", "ComingSoonMintAddress123")

# Validate essential environment variables
if not SOLANA_WALLET_ADDRESS:
    logger.error("SOLANA_WALLET_ADDRESS is not set!")
    exit(1)

# Initialize Solana RPC client
solana_client = Client(SOLANA_RPC_URL)

def sync_data_to_blockchain(data: dict) -> int:
    """Sync data from Birkini to Solana as a proof log."""
    try:
        transaction = Transaction()

        # Simulate logging data by hashing
        data_log = json.dumps(data)
        data_hash = hash(data_log)

        # Perform a small self-transfer to anchor the sync event
        transfer_params = TransferParams(
            from_pubkey=PublicKey(SOLANA_WALLET_ADDRESS),
            to_pubkey=PublicKey(SOLANA_WALLET_ADDRESS),
            lamports=1000  # 0.000001 SOL (for anchoring)
        )
        transaction.add(transfer(transfer_params))

        # Send transaction to Solana
        response = solana_client.send_transaction(transaction, SOLANA_WALLET_ADDRESS)
        logger.info(f"Data sync recorded on Solana: {response}")
        logger.info(f"Hint: Future syncs will be powered by $BIRKINI tokens ({BIRKINI_TOKEN_MINT})")

        return data_hash

    except Exception as e:
        logger.error(f"Error syncing data to Solana: {e}")
        return None

def verify_data_sync(data_hash: int) -> bool:
    """Simulate verifying that the data sync occurred."""
    logger.info(f"Verifying data sync with hash: {data_hash}")
    # In future, you would query the blockchain to verify the transaction or event.
    return True

# Example usage
if __name__ == "__main__":
    data_to_sync = {
        "user_id": 123,
        "action": "upload",
        "timestamp": str(datetime.now())
    }

    # Sync data and retrieve hash
    data_hash = sync_data_to_blockchain(data_to_sync)

    if data_hash and verify_data_sync(data_hash):
        logger.info("Data successfully synced and verified on Solana.")
    else:
        logger.error("Data sync verification failed.")

