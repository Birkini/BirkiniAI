from cryptography.fernet import Fernet
import os

# Load encryption key from environment or raise error if not found
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    raise EnvironmentError("ENCRYPTION_KEY not set in environment variables.")

# Initialize Fernet with the provided key
cipher = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

def generate_key() -> str:
    """Generate a new Fernet encryption key and return it as a UTF-8 string"""
    key = Fernet.generate_key()
    print(f"Generated encryption key: {key.decode()}")
    return key.decode()

def encrypt_data(data: str) -> str:
    """Encrypt a string and return the ciphertext as a UTF-8 string"""
    if not isinstance(data, str):
        raise TypeError("Data must be a string.")
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt a previously encrypted UTF-8 string"""
    if not isinstance(encrypted_data, str):
        raise TypeError("Encrypted data must be a string.")
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()

# Example usage
if __name__ == "__main__":
    example = "Sensitive user information"
    print("Original:", example)

    encrypted = encrypt_data(example)
    print("Encrypted:", encrypted)

    decrypted = decrypt_data(encrypted)
    print("Decrypted:", decrypted)

