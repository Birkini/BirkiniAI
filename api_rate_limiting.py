import time
import logging
from collections import defaultdict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MAX_REQUESTS = 100       # Max requests allowed
TIME_WINDOW = 3600       # Time window in seconds (1 hour)

# In-memory store of user request timestamps
user_requests = defaultdict(list)

def record_request(user_id: str) -> bool:
    """
    Record a request timestamp for a user and check rate limit.

    Args:
        user_id (str): Unique identifier for the user (e.g., IP or user ID)

    Returns:
        bool: True if request is allowed, False if rate limit exceeded
    """
    current_time = time.time()
    timestamps = user_requests[user_id]

    # Remove old timestamps
    user_requests[user_id] = [ts for ts in timestamps if current_time - ts < TIME_WINDOW]

    if len(user_requests[user_id]) >= MAX_REQUESTS:
        return False

    user_requests[user_id].append(current_time)
    return True

def handle_api_request(user_id: str) -> str:
    """
    Simulate handling an API request with rate limiting applied.

    Args:
        user_id (str): Identifier of the requesting user

    Returns:
        str: Result message
    """
    if record_request(user_id):
        logger.info(f"✅ Request from user {user_id} allowed.")
        return "Request processed successfully."
    else:
        logger.warning(f"⛔ Request from user {user_id} was rate-limited.")
        return "Rate limit exceeded. Please try again later."

# Example usage
if __name__ == "__main__":
    test_user = "user123"
    for i in range(105):
        print(handle_api_request(test_user))
        time.sleep(0.5)

