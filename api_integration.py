import os
import requests
import json
from sqlalchemy import create_engine

# Load environment configurations
API_URL = os.environ.get('API_URL', 'https://api.example.com/data')
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')

# Create SQLAlchemy engine for database interaction
engine = create_engine(DATABASE_URI)

def fetch_data_from_api():
    """Fetch data from an external API"""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()  # Convert JSON data into a Python dictionary
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def save_data_to_db(data, table_name):
    """Save fetched data to the database"""
    try:
        if data:
            # Convert data into a format compatible with the database
            # Assuming each entry in the list is a dictionary
            import pandas as pd
            df = pd.DataFrame(data)
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"Data successfully saved to the {table_name} table.")
        else:
            print("No data to save.")
    except Exception as e:
        print(f"An error occurred while saving data to the database: {e}")

def process_and_store_data():
    """Fetch, process, and store external API data"""
    # Fetch data from the API
    data = fetch_data_from_api()
    if data:
        # Process the data if necessary (e.g., filter, clean)
        # Here we just save the raw data, but you can add processing steps
        save_data_to_db(data, "external_data")

# Example usage
if __name__ == "__main__":
    process_and_store_data()
