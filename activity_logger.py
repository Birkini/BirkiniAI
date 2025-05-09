import os
import json
from datetime import datetime

# Log file path
LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 'user_activity_log.json')

def log_activity(user_id, action, details=None):
    """Log user activities to a file"""
    log_entry = {
        "user_id": user_id,
        "action": action,
        "details": details if details else "No additional details",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        # Open log file and append new log entry
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
        print(f"Activity logged for user {user_id}: {action}")
    except Exception as e:
        print(f"Error logging activity: {e}")

def get_activity_logs():
    """Retrieve all activity logs"""
    try:
        with open(LOG_FILE_PATH, 'r') as log_file:
            logs = [json.loads(line.strip()) for line in log_file.readlines()]
        return logs
    except Exception as e:
        print(f"Error reading logs: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Log some activities
    log_activity(user_id=1, action="Upload Data", details="User uploaded a dataset.")
    log_activity(user_id=2, action="Query Execution", details="User queried the 'sales' table.")
    
    # Get and print activity logs
    activity_logs = get_activity_logs()
    print("Activity Logs:")
    for log in activity_logs:
        print(log)
