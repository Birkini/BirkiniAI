import json
import re
from datetime import datetime

# Validation rules for the data fields
VALID_DATE_FORMAT = "%Y-%m-%d"  # Date should be in YYYY-MM-DD format

# Data validation functions
def validate_data_format(data):
    """Validate the general structure of the data"""
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary.")
    
    # Check if all required fields are present
    required_fields = ['user_id', 'name', 'email', 'created_at']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate email format
    if not is_valid_email(data['email']):
        raise ValueError(f"Invalid email format: {data['email']}")
    
    # Validate date format
    if not is_valid_date(data['created_at']):
        raise ValueError(f"Invalid date format for created_at: {data['created_at']}")
    
    return True

def is_valid_email(email):
    """Check if the email is valid"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_date(date_str):
    """Check if the date string is in the correct format"""
    try:
        datetime.strptime(date_str, VALID_DATE_FORMAT)
        return True
    except ValueError:
        return False

def validate_data_against_schema(data, schema):
    """Validate if the data matches the predefined schema"""
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary.")

    for field, field_type in schema.items():
        if field not in data:
            raise ValueError(f"Missing field: {field}")
        if not isinstance(data[field], field_type):
            raise ValueError(f"Invalid type for field {field}. Expected {field_type}, got {type(data[field])}.")
    
    return True

# Example usage
if __name__ == "__main__":
    # Example data to validate
    sample_data = {
        "user_id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "created_at": "2023-05-01"
    }

    # Define a schema for validation
    schema = {
        "user_id": int,
        "name": str,
        "email": str,
        "created_at": str
    }

    try:
        # Validate the sample data against the schema
        validate_data_format(sample_data)
        validate_data_against_schema(sample_data, schema)
        print("Data is valid!")
    except ValueError as e:
        print(f"Data validation failed: {e}")
