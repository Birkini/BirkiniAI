import os
import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from cryptography.fernet import Fernet

# Load environment configurations
DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///birkini.db")
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("Missing ENCRYPTION_KEY environment variable")

# Set up Fernet encryption
cipher = Fernet(ENCRYPTION_KEY)

# Initialize SQLAlchemy engine
engine = create_engine(DATABASE_URI)

def decrypt_data(value: str) -> str:
    """Decrypt a single encrypted string value."""
    try:
        return cipher.decrypt(value.encode()).decode()
    except Exception:
        return value  # Return original if decryption fails

def query_data(query: str, parameters: dict | None = None) -> list[dict]:
    """Execute a SQL query with optional parameters and return decrypted results."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), parameters or {})
            rows = result.mappings().all()

        decrypted_rows = []
        for row in rows:
            decrypted_row = {
                column: decrypt_data(str(value)) if isinstance(value, str) else value
                for column, value in row.items()
            }
            decrypted_rows.append(decrypted_row)

        return decrypted_rows

    except SQLAlchemyError as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return []

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM user_data WHERE user_id = :user_id"
    parameters = {"user_id": 1}
    result = query_data(query, parameters)
    print("Decrypted Query Results:", result)
