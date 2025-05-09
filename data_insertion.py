import os
import json
import pandas as pd
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from datetime import datetime

# Load environment configurations
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', 'your-encryption-key')

# Set up encryption
cipher = Fernet(ENCRYPTION_KEY)

# Create SQLAlchemy engine for database interaction
engine = create_engine(DATABASE_URI)

def encrypt_data(data):
    """Encrypt the data before inserting into the database"""
    return cipher.encrypt(data.encode())

def insert_data(data_file_path, table_name):
    """Insert data into the specified table after encryption"""
    try:
        # Load data from file (CSV or JSON)
        if data_file_path.endswith('.csv'):
            data = pd.read_csv(data_file_path)
        elif data_file_path.endswith('.json'):
            data = pd.read_json(data_file_path)
        else:
            raise ValueError("Unsupported file format. Only .csv and .json are supported.")

        # Encrypt each row of data
        for index, row in data.iterrows():
            encrypted_row = {column: encrypt_data(str(value)) for column, value in row.items()}
            # Convert encrypted data to JSON format for storage
            json_data = json.dumps(encrypted_row)
            
            # Insert into database
            with engine.connect() as connection:
                connection.execute(f"INSERT INTO {table_name} (data, timestamp) VALUES ('{json_data}', '{datetime.now()}')")

        print(f"Data inserted successfully into {table_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
if __name__ == '__main__':
    data_file = './data/example_data.csv'  # Path to your data file
    table_name = 'user_data'  # Name of the database table
    insert_data(data_file, table_name)
