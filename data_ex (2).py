import pandas as pd
import json
import csv
from pathlib import Path

class DataExporter:
    def __init__(self, data):
        if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
            raise ValueError("Data must be a list of dictionaries.")
        self.data = data
        self.df = pd.DataFrame(data)

    def export_csv(self, file_name: str):
        """Export data to a CSV file."""
        self.df.to_csv(file_name, index=False)
        print(f"[✓] Exported to CSV: {file_name}")

    def export_json(self, file_name: str):
        """Export data to a JSON file."""
        with open(file_name, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f"[✓] Exported to JSON: {file_name}")

    def export_excel(self, file_name: str):
        """Export data to an Excel file."""
        self.df.to_excel(file_name, index=False)
        print(f"[✓] Exported to Excel: {file_name}")

    def export_custom_csv(self, file_name: str, delimiter: str = ';'):
        """Export data to a CSV file with a custom delimiter."""
        with open(file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys(), delimiter=delimiter)
            writer.writeheader()
            writer.writerows(self.data)
        print(f"[✓] Exported to custom CSV: {file_name} (delimiter='{delimiter}')")

# Sample data (this would typically come from a DB)
sample_data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "balance": 100.00},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "balance": 250.50},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "balance": 300.75}
]

if __name__ == "__main__":
    exporter = DataExporter(sample_data)
    exporter.export_csv("users_data.csv")
    exporter.export_json("users_data.json")
    exporter.export_excel("users_data.xlsx")
    exporter.export_custom_csv("users_data_custom.csv", delimiter=';')

