import pandas as pd
import json
import csv

# Sample data (normally this would come from the database)
data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "balance": 100.00},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "balance": 250.50},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "balance": 300.75}
]

# Function to export data to CSV
def export_to_csv(data, file_name):
    """Export data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Data successfully exported to {file_name}")

# Function to export data to JSON
def export_to_json(data, file_name):
    """Export data to a JSON file."""
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully exported to {file_name}")

# Function to export data to Excel
def export_to_excel(data, file_name):
    """Export data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f"Data successfully exported to {file_name}")

# Function to export data to a custom CSV format (with custom delimiters)
def export_to_custom_csv(data, file_name, delimiter=';'):
    """Export data to a custom CSV format."""
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data successfully exported to {file_name} with delimiter {delimiter}")

# Example usage
if __name__ == "__main__":
    # Export data to CSV
    export_to_csv(data, "users_data.csv")

    # Export data to JSON
    export_to_json(data, "users_data.json")

    # Export data to Excel
    export_to_excel(data, "users_data.xlsx")

    # Export data to a custom CSV format with semicolon delimiter
    export_to_custom_csv(data, "users_data_custom.csv", delimiter=';')
