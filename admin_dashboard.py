import os
import logging
import pandas as pd
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from datetime import datetime

# Flask app setup
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///birkini.db')
engine = create_engine(DATABASE_URI)

def get_system_logs() -> list | dict:
    """Read system logs from JSON log file"""
    log_path = os.environ.get('LOG_FILE_PATH', 'system_log.json')
    try:
        with open(log_path, 'r') as f:
            return [line.strip() for line in f]
    except Exception as e:
        logger.error(f"Failed to read logs: {e}")
        return {"error": "Could not read logs."}

def get_all_users() -> list | dict:
    """Fetch all user data"""
    try:
        query = "SELECT * FROM user_data"
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        return {"error": "Could not fetch users."}

@app.route("/admin/logs", methods=["GET"])
def fetch_logs():
    return jsonify(get_system_logs()), 200

@app.route("/admin/users", methods=["GET"])
def view_users():
    return jsonify(get_all_users()), 200

@app.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM user_data WHERE user_id = :uid"), {"uid": user_id})
        logger.info(f"User {user_id} deleted.")
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify({"error": "Could not delete user."}), 500

@app.route("/admin/stats", methods=["GET"])
def get_system_stats():
    try:
        stats = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S"),
            "active_users": 1234,
            "total_requests": 5678,
            "uptime": "48 hours"
        }
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        return jsonify({"error": "Could not fetch system stats."}), 500

if __name__ == "__main__":
    app.run(debug=True)
