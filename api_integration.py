import os
import json
import logging
import requests
import pandas as pd
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Load environment configurations
API_URL = os.getenv('API_URL', 'https://api.example.com/data')
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///birkini.db')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URI)

def fetch_data_from_api():
    """Fetch data from an external API"""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        return None

def save_data_to_db(data, table_name):
    """Save JSON data to a SQL table"""
    if not data:
        logging.warning("No data to save.")
        return

    try:
        df = pd.DataFrame(data)
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logging.info(f"Data saved to '{table_name}' table.")
    except Exception as e:
        logging.error(f"Error saving data to database: {e}")

def process_and_store_data():
    """Main function to handle data flow"""
    data = fetch_data_from_api()
    save_data_to_db(data, "external_data")

if __name__ == "__main__":
    process_and_store_data()

