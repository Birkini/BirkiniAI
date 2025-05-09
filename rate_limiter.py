import time
import redis
from flask import Flask, request, jsonify
from functools import wraps

# Flask app setup
app = Flask(__name__)

# Redis setup (using localhost for simplicity)
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Rate limiting configuration
RATE_LIMIT = 100  # Max number of requests
TIME_WINDOW = 60  # Time window in seconds (1 minute)

# Decorator to enforce rate limit
def rate_limit(limit=RATE_LIMIT, window=TIME_WINDOW):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_ip = request.remote_addr  # Get the user's IP address
            current_time = int(time.time())  # Get current time in seconds

            # Create a unique key for the user's IP and the current time window
            key = f"rate_limit:{user_ip}:{current_time // window}"

            # Check if the user has exceeded the limit
            request_count = r.get(key)

            if request_count is None:
                # If no count, set the initial count to 1
                r.setex(key, window, 1)
            elif int(request_count) < limit:
                # If under limit, increment the count
                r.incr(key)
            else:
                # If limit is reached, deny access
                return jsonify({"error": "Rate limit exceeded, try again later"}), 429

            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/api/resource', methods=['GET'])
@rate_limit()  # Apply rate limiting to this route
def get_resource():
    return jsonify({"message": "Successfully accessed the resource!"})

@app.route('/api/reset', methods=['POST'])
def reset_rate_limits():
    """Manually reset the rate limit for all users."""
    r.flushdb()  # This will delete all keys in the current database
    return jsonify({"message": "Rate limits have been reset"}), 200

if __name__ == "__main__":
    app.run(debug=True)
