import os
import pandas as pd
from sqlalchemy import create_engine

# Database URI configuration
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
engine = create_engine(DATABASE_URI)

def import_csv(file_path, table_name):
    """Import CSV data into a database table"""
    try:
        data = pd.read_csv(file_path)
        data.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"CSV data from {file_path} imported into {table_name} table.")
    except Exception as e:
        print(f"Error importing CSV: {e}")

def import_json(file_path, table_name):
    """Import JSON data into a database table"""
    try:
        data = pd.read_json(file_path)
        data.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"JSON data from {file_path} imported into {table_name} table.")
    except Exception as e:
        print(f"Error importing JSON: {e}")

def import_excel(file_path, table_name):
    """Import Excel data into a database table"""
    try:
        data = pd.read_excel(file_path)
        data.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Excel data from {file_path} imported into {table_name} table.")
    except Exception as e:
        print(f"Error importing Excel: {e}")

def import_data(file_path, file_type, table_name):
    """Generalized function for importing data from different formats"""
    if file_type == 'csv':
        import_csv(file_path, table_name)
    elif file_type == 'json':
        import_json(file_path, table_name)
    elif file_type == 'excel':
        import_excel(file_path, table_name)
    else:
        print(f"Unsupported file type: {file_type}")

# Example usage
if __name__ == "__main__":
    # Example: Importing CSV data into a 'users' table
    import_data('path/to/your/file.csv', 'csv', 'users')

    # Example: Importing JSON data into a 'transactions' table
    import_data('path/to/your/file.json', 'json', 'transactions')

    # Example: Importing Excel data into a 'products' table
    import_data('path/to/your/file.xlsx', 'excel', 'products')
