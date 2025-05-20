import os
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

class DataImporter:
    def __init__(self, db_uri=None):
        self.database_uri = db_uri or os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
        self.engine = create_engine(self.database_uri)

    def import_file(self, file_path, table_name):
        """Determine file type and import accordingly."""
        ext = Path(file_path).suffix.lower()
        if ext == '.csv':
            return self._import_csv(file_path, table_name)
        elif ext == '.json':
            return self._import_json(file_path, table_name)
        elif ext in ['.xls', '.xlsx']:
            return self._import_excel(file_path, table_name)
        else:
            print(f"[!] Unsupported file type: {ext}")
            return

    def _import_csv(self, file_path, table_name):
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
            print(f"[✓] CSV imported into '{table_name}' from: {file_path}")
        except Exception as e:
            print(f"[✗] Failed to import CSV: {e}")

    def _import_json(self, file_path, table_name):
        try:
            df = pd.read_json(file_path)
            df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
            print(f"[✓] JSON imported into '{table_name}' from: {file_path}")
        except Exception as e:
            print(f"[✗] Failed to import JSON: {e}")

    def _import_excel(self, file_path, table_name):
        try:
            df = pd.read_excel(file_path)
            df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
            print(f"[✓] Excel imported into '{table_name}' from: {file_path}")
        except Exception as e:
            print(f"[✗] Failed to import Excel: {e}")

# Example usage
if __name__ == "__main__":
    importer = DataImporter()

    # Replace these paths with real ones
    importer.import_file('path/to/your/file.csv', 'users')
    importer.import_file('path/to/your/file.json', 'transactions')
    importer.import_file('path/to/your/file.xlsx', 'products')
