import os
import shutil
import time
from datetime import datetime
from pathlib import Path

# Configuration settings
BACKUP_DIR = Path("/path/to/backup/directory")
SOURCE_DIR = Path("/path/to/your/data/directory")
BACKUP_RETENTION_DAYS = 7  # Number of days to keep backups

def perform_backup():
    """Create a timestamped backup of the source directory."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = BACKUP_DIR / f"backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)

        for item in SOURCE_DIR.iterdir():
            target = backup_path / item.name
            if item.is_dir():
                shutil.copytree(item, target)
            else:
                shutil.copy2(item, target)

        print(f"✅ Backup completed: {backup_path}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")

def cleanup_old_backups():
    """Remove backup folders older than the retention policy allows."""
    try:
        now = time.time()
        for folder in BACKUP_DIR.iterdir():
            if folder.is_dir():
                age_days = (now - folder.stat().st_ctime) / (3600 * 24)
                if age_days > BACKUP_RETENTION_DAYS:
                    shutil.rmtree(folder)
                    print(f"🗑️ Deleted old backup: {folder}")
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    perform_backup()
    cleanup_old_backups()
