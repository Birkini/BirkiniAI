import pandas as pd
from cerberus import Validator

# Define the schema for validating incoming data
schema = {
    'id': {'type': 'integer', 'min': 1},
    'name': {'type': 'string', 'minlength': 1, 'maxlength': 255},
    'email': {'type': 'string', 'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
    'age': {'type': 'integer', 'min': 18, 'max': 120}
}

# Function to validate the data
def validate_data(data):
    """Validate the incoming data against the predefined schema."""
    validator = Validator(schema)
    if validator.validate(data):
        print("Data is valid")
        return True
    else:
        print(f"Data validation failed: {validator.errors}")
        return False

# Example function to ingest data
def ingest_data(data):
    """Simulate data ingestion process."""
    if validate_data(data):
        # In a real scenario, the data would be saved to the database
        print("Ingesting data...")
        # Simulating a successful data ingestion
        return "Data ingested successfully"
    else:
        return "Data ingestion failed due to validation errors"

# Sample data
data = {
    'id': 1,
    'name': 'Alice',
    'email': 'alice@example.com',
    'age': 30
}

# Ingesting the data
result = ingest_data(data)
print(result)

# Example of invalid data
invalid_data = {
    'id': -1,  # Invalid ID
    'name': '',  # Invalid name
    'email': 'invalid-email',  # Invalid email
    'age': 17  # Invalid age (too young)
}

# Ingesting the invalid data
invalid_result = ingest_data(invalid_data)
print(invalid_result)
