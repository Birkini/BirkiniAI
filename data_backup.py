import os
import shutil
import datetime
from pathlib import Path
from typing import Optional

# Backup and data directories (read from environment or use defaults)
BACKUP_DIRECTORY = Path(os.getenv("BACKUP_DIRECTORY", "/path/to/backup"))
DATA_DIRECTORY = Path(os.getenv("DATA_DIRECTORY", "/path/to/data"))

def create_backup() -> None:
    """Create a timestamped backup of the data directory."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = BACKUP_DIRECTORY / f"backup_{timestamp}"

        if not DATA_DIRECTORY.exists():
            print(f"Data directory {DATA_DIRECTORY} does not exist.")
            return

        shutil.copytree(DATA_DIRECTORY, backup_path)
        print(f"✅ Backup created at {backup_path}")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")

def list_backups() -> None:
    """List all backup directories."""
    try:
        if not BACKUP_DIRECTORY.exists():
            print(f"Backup directory {BACKUP_DIRECTORY} does not exist.")
            return

        backups = sorted([d.name for d in BACKUP_DIRECTORY.iterdir() if d.is_dir()])
        if not backups:
            print("No backups found.")
            return

        print("📦 Available backups:")
        for backup in backups:
            print(f"  • {backup}")
    except Exception as e:
        print(f"❌ Error listing backups: {e}")

def restore_backup(backup_name: str) -> None:
    """Restore the specified backup to the data directory."""
    try:
        backup_path = BACKUP_DIRECTORY / backup_name

        if not backup_path.exists() or not backup_path.is_dir():
            print(f"Backup '{backup_name}' does not exist.")
            return

        if not DATA_DIRECTORY.exists():
            DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

        shutil.copytree(backup_path, DATA_DIRECTORY, dirs_exist_ok=True)
        print(f"✅ Data restored from {backup_path}")
    except Exception as e:
        print(f"❌ Failed to restore backup: {e}")

# Example usage
if __name__ == "__main__":
    create_backup()
    list_backups()
    # Replace with actual backup folder name when testing
    restore_backup("backup_2023-05-01_10-00-00")
