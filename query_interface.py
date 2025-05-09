import sqlite3
import pandas as pd

# Database connection
DATABASE = "birkini.db"

def connect_db():
    """Connect to the Birkini database."""
    conn = sqlite3.connect(DATABASE)
    return conn

def execute_query(query, params=None):
    """Execute an SQL query and return results as a pandas DataFrame."""
    conn = connect_db()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

def display_results(df):
    """Display the query results in a user-friendly format."""
    if df is not None and not df.empty:
        print(df.head())
    else:
        print("No results to display.")

def get_all_users():
    """Fetch all users from the users table."""
    query = "SELECT * FROM users"
    result = execute_query(query)
    display_results(result)

def get_transactions_by_user(user_id):
    """Fetch transactions for a specific user."""
    query = "SELECT * FROM transactions WHERE user_id = ?"
    result = execute_query(query, (user_id,))
    display_results(result)

def create_transaction(user_id, amount, date):
    """Insert a new transaction into the transactions table."""
    query = "INSERT INTO transactions (user_id, amount, date) VALUES (?, ?, ?)"
    execute_query(query, (user_id, amount, date))

# Example usage
if __name__ == "__main__":
    # Example: Fetch all users
    get_all_users()

    # Example: Fetch transactions for a specific user
    get_transactions_by_user(1)

    # Example: Insert a new transaction
    create_transaction(1, 200.00, "2023-05-01")
