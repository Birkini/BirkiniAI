import os
import logging
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from config import Config

# === Logging Configuration ===
logger = logging.getLogger("BirkiniDataPipeline")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# === Database Engine Initialization ===
def get_db_engine():
    """Create and return a SQLAlchemy engine."""
    try:
        return create_engine(Config.DATABASE_URI)
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise

# === Data Validation ===
def validate_data(data: pd.DataFrame) -> None:
    """Ensure the input is a non-empty DataFrame."""
    if not isinstance(data, pd.DataFrame):
        logger.error("Invalid input: Expected a Pandas DataFrame.")
        raise TypeError("Data must be a Pandas DataFrame.")
    if data.empty:
        logger.error("Received an empty DataFrame.")
        raise ValueError("Data is empty.")
    logger.info("Data validated successfully.")

# === Insert Logic ===
def insert_data(table_name: str, data: pd.DataFrame) -> None:
    """Insert data into the specified database table."""
    validate_data(data)
    try:
        engine = get_db_engine()
        with engine.begin() as connection:
            data.to_sql(table_name, con=connection, if_exists='append', index=False)
        logger.info(f"Inserted data into '{table_name}' successfully at {datetime.now()}")
    except SQLAlchemyError as e:
        logger.exception(f"SQLAlchemy error while inserting data into '{table_name}': {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error while inserting data into '{table_name}': {e}")
        raise

# === Push Function ===
def push_data_to_birkini(data: pd.DataFrame, table_name: str = "dataset_table") -> None:
    """Push validated data to Birkini's designated table."""
    try:
        insert_data(table_name, data)
        logger.info("Data successfully pushed to Birkini.")
    except Exception as e:
        logger.error(f"Failed to push data to Birkini: {e}")
        raise

# === Sample Execution ===
def main():
    sample_data = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "score": [95, 88, 76]
    })

    push_data_to_birkini(sample_data)

if __name__ == "__main__":
    main()
