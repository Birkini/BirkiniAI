import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "user_activity_log.json")

def _ensure_log_file() -> None:
    """Ensure the log file and its directory exist."""
    dir_path = os.path.dirname(LOG_FILE_PATH)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    if not os.path.isfile(LOG_FILE_PATH):
        open(LOG_FILE_PATH, 'w', encoding='utf-8').close()

def log_activity(user_id: int, action: str, details: Optional[str] = None) -> None:
    """Log a user action with a UTC timestamp."""
    _ensure_log_file()
    log_entry = {
        "user_id": user_id,
        "action": action,
        "details": details or "",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as file:
            json.dump(log_entry, file)
            file.write('\n')
    except Exception as e:
        raise RuntimeError(f"Failed to write log entry: {e}")

def get_activity_logs() -> List[Dict[str, str]]:
    """Return all activity log entries as a list of dictionaries."""
    if not os.path.isfile(LOG_FILE_PATH):
        return []

    logs = []
    try:
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        raise RuntimeError(f"Failed to read log file: {e}")

    return logs

# Example usage
if __name__ == "__main__":
    log_activity(1, "upload_data", "User uploaded dataset to workspace")
    log_activity(2, "query_execution", "Queried analytics from 'sales' table")
    for log in get_activity_logs():
        print(log)

