import time
from collections import defaultdict

# Set the maximum number of requests a user can make in a given time frame
MAX_REQUESTS = 100  # Max requests per time window
TIME_WINDOW = 3600  # Time window in seconds (e.g., 3600s = 1 hour)

# Store request counts per user (or IP address)
user_requests = defaultdict(list)

def record_request(user_id):
    """Record a user's request and enforce rate limiting."""
    current_time = time.time()
    
    # Clean up expired requests (older than the time window)
    user_requests[user_id] = [timestamp for timestamp in user_requests[user_id] if current_time - timestamp < TIME_WINDOW]
    
    # Check if the user has exceeded the request limit
    if len(user_requests[user_id]) >= MAX_REQUESTS:
        return False  # Rate limit exceeded
    else:
        user_requests[user_id].append(current_time)
        return True  # Request allowed

def handle_api_request(user_id):
    """Simulate handling an API request while enforcing rate limiting."""
    if record_request(user_id):
        print(f"Request from user {user_id} is allowed.")
        # Process the request (e.g., return data, execute query, etc.)
        return "Request processed successfully."
    else:
        print(f"Request from user {user_id} has been rate-limited.")
        # Handle the rate-limiting scenario (e.g., send an error message)
        return "Rate limit exceeded. Please try again later."

# Example usage
if __name__ == "__main__":
    user_id = "user123"

    # Simulate multiple requests
    for i in range(105):
        response = handle_api_request(user_id)
        print(response)
        time.sleep(0.5)  # Simulate a small delay between requests
