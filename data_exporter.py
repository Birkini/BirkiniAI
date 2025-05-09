import os
import pandas as pd
from sqlalchemy import create_engine
import json
import csv

# Load environment configurations
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')

# Create SQLAlchemy engine for database interaction
engine = create_engine(DATABASE_URI)

def export_to_csv(table_name, file_name):
    """Export data from a table to a CSV file"""
    try:
        # Query the data from the database
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, engine)

        # Save the data to a CSV file
        data.to_csv(file_name, index=False)
        print(f"Data successfully exported to {file_name}")
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")

def export_to_json(table_name, file_name):
    """Export data from a table to a JSON file"""
    try:
        # Query the data from the database
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, engine)

        # Convert data to JSON and write to file
        data_json = data.to_json(orient='records', lines=True)
        with open(file_name, 'w') as json_file:
            json_file.write(data_json)

        print(f"Data successfully exported to {file_name}")
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")

def export_custom_query(query, file_name, format='csv'):
    """Export data using a custom SQL query"""
    try:
        # Query the data using the custom SQL query
        data = pd.read_sql(query, engine)

        # Export based on desired format
        if format == 'csv':
            data.to_csv(file_name, index=False)
        elif format == 'json':
            data_json = data.to_json(orient='records', lines=True)
            with open(file_name, 'w') as json_file:
                json_file.write(data_json)
        else:
            print("Unsupported format. Please choose 'csv' or 'json'.")

        print(f"Data successfully exported to {file_name}")
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")

# Example usage
if __name__ == "__main__":
    # Export all data from 'user_data' table to CSV
    export_to_csv('user_data', 'user_data_export.csv')

    # Export all data from 'user_data' table to JSON
    export_to_json('user_data', 'user_data_export.json')

    # Export data using custom SQL query to CSV
    custom_query = "SELECT user_id, name FROM user_data WHERE active = 1"
    export_custom_query(custom_query, 'active_users.csv', format='csv')
