import os
import json
import pandas as pd
from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import create_engine, text
from datetime import datetime

# Load configurations securely
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable not set")

try:
    cipher = Fernet(ENCRYPTION_KEY)
except Exception as e:
    raise ValueError("Invalid ENCRYPTION_KEY format for Fernet. Must be a 32-byte base64-encoded key.") from e

# Set up database connection
engine = create_engine(DATABASE_URI)

def encrypt_data(value: str) -> str:
    """Encrypt a string using Fernet"""
    return cipher.encrypt(value.encode()).decode()

def insert_data(data_file_path: str, table_name: str):
    """Encrypt and insert data from a file into the specified SQL table."""
    try:
        # Load input file
        if data_file_path.endswith('.csv'):
            data = pd.read_csv(data_file_path)
        elif data_file_path.endswith('.json'):
            data = pd.read_json(data_file_path)
        else:
            raise ValueError("Unsupported file format. Use .csv or .json")

        with engine.begin() as connection:
            for _, row in data.iterrows():
                try:
                    encrypted_row = {col: encrypt_data(str(val).strip()) for col, val in row.items()}
                    payload = json.dumps(encrypted_row)
                    timestamp = datetime.utcnow().isoformat()

                    sql = text(f"""
                        INSERT INTO {table_name} (data, timestamp)
                        VALUES (:data, :timestamp)
                    """)
                    connection.execute(sql, {"data": payload, "timestamp": timestamp})
                except (InvalidToken, Exception) as row_error:
                    print(f"Failed to encrypt/insert row: {row.to_dict()} — Error: {row_error}")

        print(f"✅ Data inserted successfully into '{table_name}'")

    except Exception as main_error:
        print(f"❌ An error occurred: {main_error}")

# Example usage
if __name__ == '__main__':
    data_file = './data/example_data.csv'
    table_name = 'user_data'
    insert_data(data_file, table_name)
