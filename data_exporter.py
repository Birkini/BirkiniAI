import os
import pandas as pd
from sqlalchemy import create_engine

# Load environment configurations
DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///birkini.db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URI)

def export_to_csv(table_name: str, file_name: str) -> None:
    """Export entire table to CSV"""
    try:
        data = pd.read_sql(f"SELECT * FROM {table_name}", engine)
        data.to_csv(file_name, index=False)
        print(f"Exported data to CSV: {file_name}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

def export_to_json(table_name: str, file_name: str) -> None:
    """Export entire table to JSON"""
    try:
        data = pd.read_sql(f"SELECT * FROM {table_name}", engine)
        data.to_json(file_name, orient="records", lines=True)
        print(f"Exported data to JSON: {file_name}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

def export_custom_query(query: str, file_name: str, format: str = "csv") -> None:
    """Export results from a custom SQL query to CSV or JSON"""
    try:
        data = pd.read_sql(query, engine)
        if format == "csv":
            data.to_csv(file_name, index=False)
        elif format == "json":
            data.to_json(file_name, orient="records", lines=True)
        else:
            raise ValueError("Unsupported format. Use 'csv' or 'json'.")
        print(f"Exported query results to {file_name}")
    except Exception as e:
        print(f"Error exporting custom query: {e}")

# Example usage
if __name__ == "__main__":
    export_to_csv("user_data", "user_data_export.csv")
    export_to_json("user_data", "user_data_export.json")
    export_custom_query(
        "SELECT user_id, name FROM user_data WHERE active = 1",
        "active_users.csv",
        format="csv"
    )

