import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

LOG_FILE_PATH: str = os.getenv('LOG_FILE_PATH', 'user_activity_log.json')

def _ensure_log_file():
    """Ensure that the log file and its directory exist."""
    directory = os.path.dirname(LOG_FILE_PATH)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(LOG_FILE_PATH):
        open(LOG_FILE_PATH, 'a', encoding='utf-8').close()

def log_activity(user_id: int, action: str, details: Optional[str] = None) -> None:
    """
    Append a new activity log entry as JSON to the log file.

    :param user_id: Identifier of the user who performed the action
    :param action: Description of the action performed
    :param details: Additional details about the action
    """
    _ensure_log_file()
    entry: Dict[str, Any] = {
        "user_id": user_id,
        "action": action,
        "details": details or "",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    try:
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
    except IOError as e:
        raise RuntimeError(f"Failed to write to log file {LOG_FILE_PATH}: {e}") from e

def get_activity_logs() -> List[Dict[str, Any]]:
    """
    Read and parse all log entries from the log file.

    :return: List of log entry dictionaries
    """
    if not os.path.exists(LOG_FILE_PATH):
        return []
    logs: List[Dict[str, Any]] = []
    try:
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return logs
    except IOError as e:
        raise RuntimeError(f"Failed to read log file {LOG_FILE_PATH}: {e}") from e

# Example usage
if __name__ == '__main__':
    log_activity(1, "upload_data", "User uploaded a dataset")
    log_activity(2, "query_execution", "User queried the sales table")
    for entry in get_activity_logs():
        print(entry)

