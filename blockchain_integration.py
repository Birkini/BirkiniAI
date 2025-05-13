import os
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.rpc.types import TxOpts
from base58 import b58decode

# Environment setup
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
SOLANA_PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")  # Must be a base58-encoded secret key

if not SOLANA_PRIVATE_KEY:
    raise EnvironmentError("Missing SOLANA_PRIVATE_KEY in environment variables")

# Load wallet keypair
wallet_keypair = Keypair.from_secret_key(b58decode(SOLANA_PRIVATE_KEY))
wallet_pubkey = wallet_keypair.public_key

# Set up Solana client
solana_client = Client(SOLANA_RPC_URL)

def get_balance():
    """Fetch wallet balance in lamports from Solana blockchain."""
    response = solana_client.get_balance(wallet_pubkey)
    if response.get("result"):
        return response["result"]["value"]
    raise ValueError("Failed to fetch balance")

def record_transaction(note: str):
    """
    Record a transaction on-chain by transferring a small amount to self.
    This acts as an on-chain proof-of-event marker.
    """
    transaction = Transaction()
    transaction.add(
        transfer(
            TransferParams(
                from_pubkey=wallet_pubkey,
                to_pubkey=wallet_pubkey,
                lamports=1000  # Small value to trigger an on-chain record
            )
        )
    )

    try:
        response = solana_client.send_transaction(transaction, wallet_keypair, opts=TxOpts(skip_confirmation=False))
        return response
    except Exception as e:
        return {"error": str(e)}

def verify_data_on_chain(data_hash: str):
    """
    Placeholder function to simulate data integrity check.
    In real use, you'd store the hash on-chain (e.g., via memo program).
    """
    current_balance = get_balance()
    print(f"[Simulated] Verifying hash '{data_hash}' against chain state.")
    print(f"Current wallet balance: {current_balance} lamports")
    return current_balance

# Example usage
if __name__ == "__main__":
    print("Recording transaction on-chain...")
    result = record_transaction("Log data event")
    print("Transaction result:", result)

    test_hash = "example-data-hash"
    verify_data_on_chain(test_hash)

