import os
import json
from sqlalchemy import create_engine, text
from cryptography.fernet import Fernet

# Load environment configurations
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', 'your-encryption-key')

# Set up encryption
cipher = Fernet(ENCRYPTION_KEY)

# Create SQLAlchemy engine for database interaction
engine = create_engine(DATABASE_URI)

def decrypt_data(data):
    """Decrypt the data before returning it"""
    return cipher.decrypt(data.encode()).decode()

def query_data(query, parameters=None):
    """Execute a query on the Birkini database and return the results"""
    try:
        # If parameters are provided, execute the query with parameters
        if parameters:
            result = engine.execute(text(query), parameters)
        else:
            result = engine.execute(text(query))

        rows = result.fetchall()
        # Decrypt the data from each row
        decrypted_rows = []
        for row in rows:
            decrypted_row = {column: decrypt_data(str(value)) for column, value in row.items()}
            decrypted_rows.append(decrypted_row)

        return decrypted_rows

    except Exception as e:
        print(f"Error executing query: {e}")
        return []

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM user_data WHERE user_id = :user_id"
    parameters = {'user_id': 1}  # Example parameter
    result = query_data(query, parameters)
    print("Decrypted Query Results:", result)
