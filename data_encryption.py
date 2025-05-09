from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# Secret key for encryption - In a real application, store this securely, not in the code
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-32-byte-secret-key')

def pad_data(data):
    """Pad data to ensure it's a multiple of 16 bytes (required for AES encryption)"""
    block_size = 16
    padding_length = block_size - len(data) % block_size
    return data + (chr(padding_length) * padding_length).encode()

def encrypt_data(data):
    """Encrypt the given data using AES (CBC mode)"""
    cipher = AES.new(SECRET_KEY.encode(), AES.MODE_CBC)
    padded_data = pad_data(data.encode())
    ciphertext = cipher.encrypt(padded_data)

    # Return the IV (Initialization Vector) and ciphertext, base64 encoded for storage
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')

    return iv, ciphertext

def decrypt_data(iv, ciphertext):
    """Decrypt the given data using AES (CBC mode)"""
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)

    cipher = AES.new(SECRET_KEY.encode(), AES.MODE_CBC, iv=iv)
    padded_data = cipher.decrypt(ciphertext)

    # Remove padding
    padding_length = padded_data[-1]
    data = padded_data[:-padding_length].decode()

    return data

# Example usage
if __name__ == "__main__":
    # Encrypt some data
    data_to_encrypt = "This is sensitive data that needs to be encrypted."
    iv, encrypted_data = encrypt_data(data_to_encrypt)
    print(f"Encrypted data: {encrypted_data}")

    # Decrypt the data
    decrypted_data = decrypt_data(iv, encrypted_data)
    print(f"Decrypted data: {decrypted_data}")
