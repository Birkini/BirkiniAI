from cryptography.fernet import Fernet
import os

# Load the encryption key (must be stored securely)
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', 'your-encryption-key')

# Initialize the Fernet encryption system
cipher = Fernet(ENCRYPTION_KEY)

def generate_key():
    """Generate a new encryption key (use this once and store securely)"""
    key = Fernet.generate_key()
    print(f"Your new encryption key: {key.decode()}")
    return key

def encrypt_data(data: str) -> str:
    """Encrypt data using the Fernet symmetric encryption"""
    if isinstance(data, str):
        data = data.encode()  # Ensure the data is in bytes
    encrypted_data = cipher.encrypt(data)
    return encrypted_data.decode()  # Return as string for ease of storage

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data using the Fernet symmetric encryption"""
    encrypted_data = encrypted_data.encode()  # Ensure the data is in bytes
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data.decode()  # Return as string

# Example usage
if __name__ == "__main__":
    # Example data to encrypt and decrypt
    sample_data = "Sensitive user information here"

    print("Original data:", sample_data)

    # Encrypt data
    encrypted_data = encrypt_data(sample_data)
    print("Encrypted data:", encrypted_data)

    # Decrypt data
    decrypted_data = decrypt_data(encrypted_data)
    print("Decrypted data:", decrypted_data)
