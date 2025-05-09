import os
import shutil
import datetime

# Backup directory path (configure the path based on your system or cloud setup)
BACKUP_DIRECTORY = os.environ.get('BACKUP_DIRECTORY', '/path/to/backup')

# Directory that holds the data to be backed up
DATA_DIRECTORY = os.environ.get('DATA_DIRECTORY', '/path/to/data')

def create_backup():
    """Create a backup of the data directory."""
    try:
        # Get the current timestamp for backup folder naming
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = os.path.join(BACKUP_DIRECTORY, f"backup_{timestamp}")

        # Create the backup folder
        os.makedirs(backup_path, exist_ok=True)

        # Copy the data directory to the backup location
        shutil.copytree(DATA_DIRECTORY, backup_path)
        print(f"Backup created successfully at {backup_path}")
    except Exception as e:
        print(f"Error during backup: {e}")

def list_backups():
    """List all available backups."""
    try:
        # List all folders in the backup directory
        backups = os.listdir(BACKUP_DIRECTORY)
        print("Available backups:")
        for backup in backups:
            print(backup)
    except Exception as e:
        print(f"Error listing backups: {e}")

def restore_backup(backup_name):
    """Restore data from a specific backup."""
    try:
        backup_path = os.path.join(BACKUP_DIRECTORY, backup_name)
        if not os.path.exists(backup_path):
            print(f"Backup {backup_name} does not exist.")
            return

        # Restore the data from the backup directory
        shutil.copytree(backup_path, DATA_DIRECTORY, dirs_exist_ok=True)
        print(f"Data restored successfully from {backup_path}")
    except Exception as e:
        print(f"Error restoring backup: {e}")

# Example usage
if __name__ == "__main__":
    # Create a backup
    create_backup()

    # List available backups
    list_backups()

    # Restore a backup (replace with an actual backup name)
    restore_backup("backup_2023-05-01_10-00-00")
