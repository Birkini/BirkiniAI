import os
import shutil
import time
from datetime import datetime

# Configuration settings
BACKUP_DIR = "/path/to/backup/directory"
SOURCE_DIR = "/path/to/your/data/directory"
BACKUP_RETENTION_DAYS = 7  # Keep backups for the last 7 days

# Helper function to perform the backup
def perform_backup():
    """Backup the data to a specific directory."""
    try:
        # Get the current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_folder = os.path.join(BACKUP_DIR, f"backup_{current_time}")
        
        # Create the backup folder
        os.makedirs(backup_folder, exist_ok=True)
        
        # Copy all files from the source directory to the backup directory
        for item in os.listdir(SOURCE_DIR):
            source_item = os.path.join(SOURCE_DIR, item)
            backup_item = os.path.join(backup_folder, item)
            
            if os.path.isdir(source_item):
                shutil.copytree(source_item, backup_item)
            else:
                shutil.copy2(source_item, backup_item)
        
        print(f"Backup completed successfully: {backup_folder}")
    except Exception as e:
        print(f"Error during backup: {str(e)}")

# Helper function to delete old backups based on retention policy
def cleanup_old_backups():
    """Delete backups older than the retention period."""
    try:
        current_time = time.time()
        for folder in os.listdir(BACKUP_DIR):
            folder_path = os.path.join(BACKUP_DIR, folder)
            if os.path.isdir(folder_path):
                folder_creation_time = os.path.getctime(folder_path)
                age_in_days = (current_time - folder_creation_time) / (3600 * 24)
                
                if age_in_days > BACKUP_RETENTION_DAYS:
                    shutil.rmtree(folder_path)
                    print(f"Deleted old backup: {folder_path}")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

# Schedule the backup and cleanup tasks (can be scheduled with cron or Windows Task Scheduler)
if __name__ == "__main__":
    # Perform the backup and cleanup on each run
    perform_backup()
    cleanup_old_backups()
