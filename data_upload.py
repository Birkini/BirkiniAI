import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import Config
import logging

# Set up logging configuration
logger = logging.getLogger(__name__)

# Connect to the database
def get_db_engine():
    engine = create_engine(Config.DATABASE_URI)
    return engine

# Function to validate data format
def validate_data(data):
    if not isinstance(data, pd.DataFrame):
        logger.error("Invalid data format: Expected DataFrame")
        raise ValueError("Data must be a Pandas DataFrame")
    if data.empty:
        logger.error("Empty data received")
        raise ValueError("Data is empty")
    logger.info("Data validated successfully")

# Function to insert data into the database
def insert_data(table_name, data):
    try:
        validate_data(data)
        engine = get_db_engine()
        
        # Insert data into the table
        data.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info(f"Data inserted into {table_name} at {datetime.now()}")
        
    except SQLAlchemyError as e:
        logger.error(f"Error inserting data into {table_name}: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

# Example function to push a dataset
def push_data_to_birkini(data, table_name="dataset_table"):
    try:
        insert_data(table_name, data)
        logger.info("Data push to Birkini successful.")
    except Exception as e:
        logger.error(f"Failed to push data to Birkini: {e}")
        raise

# Example Usage
if __name__ == "__main__":
    # Sample data to be inserted (this can come from any source)
    sample_data = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "score": [95, 88, 76]
    })

    push_data_to_birkini(sample_data)
