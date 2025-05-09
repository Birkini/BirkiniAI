import os
import pandas as pd
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from datetime import datetime

# Flask application setup
app = Flask(__name__)

# Database URI
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
engine = create_engine(DATABASE_URI)

# Helper function to fetch logs
def get_system_logs():
    """Fetch system logs for monitoring purposes"""
    log_file_path = os.environ.get('LOG_FILE_PATH', 'system_log.json')
    try:
        with open(log_file_path, 'r') as file:
            logs = [line.strip() for line in file.readlines()]
        return logs
    except Exception as e:
        return {"error": f"Could not read logs: {str(e)}"}

# Helper function to get all users from the database
def get_all_users():
    """Fetch all users from the user_data table"""
    try:
        query = "SELECT * FROM user_data"
        users = pd.read_sql(query, engine)
        return users.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Could not fetch users: {str(e)}"}

# Admin route to get system logs
@app.route("/admin/logs", methods=["GET"])
def fetch_logs():
    logs = get_system_logs()
    return jsonify(logs), 200

# Admin route to view all users
@app.route("/admin/users", methods=["GET"])
def view_users():
    users = get_all_users()
    return jsonify(users), 200

# Admin route to delete a user by user ID
@app.route("/admin/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        with engine.connect() as conn:
            result = conn.execute(f"DELETE FROM user_data WHERE user_id = {user_id}")
            return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Could not delete user {user_id}: {str(e)}"}), 500

# Admin route to view system stats
@app.route("/admin/stats", methods=["GET"])
def get_system_stats():
    try:
        # Example system stats (extend with actual metrics like CPU usage, RAM, etc.)
        stats = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "active_users": 1234,
            "total_requests": 5678,
            "uptime": "48 hours"
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Could not fetch system stats: {str(e)}"}), 500

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)
