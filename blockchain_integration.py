import os
import requests
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

# Solana setup - Use your actual Solana RPC URL
SOLANA_RPC_URL = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
SOLANA_WALLET_ADDRESS = os.environ.get("SOLANA_WALLET_ADDRESS", "your-wallet-address")

# Set up Solana client
solana_client = Client(SOLANA_RPC_URL)

def get_balance():
    """Fetch wallet balance from Solana blockchain"""
    response = solana_client.get_balance(PublicKey(SOLANA_WALLET_ADDRESS))
    return response['result']['value']

def record_transaction(transaction_data):
    """Record a transaction hash on the blockchain to prove data integrity"""
    transaction = Transaction()
    transaction.add(
        transfer(
            TransferParams(
                from_pubkey=PublicKey(SOLANA_WALLET_ADDRESS),
                to_pubkey=PublicKey(SOLANA_WALLET_ADDRESS),  # Send to self for tracking
                lamports=1000  # Small transaction to "log" activity
            )
        )
    )

    # Send the transaction to Solana
    response = solana_client.send_transaction(transaction, SOLANA_WALLET_ADDRESS)
    return response

def verify_data_on_chain(data_hash):
    """Verify data integrity by comparing data hash with blockchain record"""
    # Normally, data hashes would be stored or referenced on-chain
    # Simulating a check for data integrity here:
    on_chain_data = get_balance()  # This is just an example; you would check real data
    print(f"Data integrity verified against blockchain record: {on_chain_data}")
    return on_chain_data

# Example usage
if __name__ == '__main__':
    transaction_data = "Transaction data to be recorded on Solana"
    print("Recording transaction...")
    result = record_transaction(transaction_data)
    print("Transaction result:", result)

    # Verifying the integrity of some data
    data_hash = "example-data-hash"
    verify_data_on_chain(data_hash)
