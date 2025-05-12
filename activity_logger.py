import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "user_activity_log.json")

def _ensure_log_file() -> None:
    """Create the log file and its directory if they do not exist."""
    directory = os.path.dirname(LOG_FILE_PATH)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    if not os.path.isfile(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w', encoding='utf-8'):
            pass

def log_activity(user_id: int, action: str, details: Optional[str] = None) -> None:
    """
    Write a log entry to the activity log.

    Parameters:
        user_id (int): ID of the user
        action (str): The action performed
        details (Optional[str]): Extra info (optional)
    """
    _ensure_log_file()
    log_entry: Dict[str, Any] = {
        "user_id": user_id,
        "action": action,
        "details": details or "",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as file:
            json.dump(log_entry, file)
            file.write('\n')
    except OSError as error:
        raise RuntimeError(f"Error writing to log file: {error}")

def get_activity_logs() -> List[Dict[str, Any]]:
    """
    Retrieve all log entries as a list of dictionaries.

    Returns:
        List[Dict[str, Any]]: Parsed logs
    """
    if not os.path.isfile(LOG_FILE_PATH):
        return []

    logs: List[Dict[str, Any]] = []
    try:
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError as error:
        raise RuntimeError(f"Error reading log file: {error}")

    return logs

# Example usage
if __name__ == "__main__":
    log_activity(1, "upload_data", "User uploaded dataset to workspace")
    log_activity(2, "query_execution", "Queried analytics from 'sales' table")
    for log in get_activity_logs():
        print(log)

