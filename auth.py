import os
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# Load the secret key for JWT (keep this private)
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

# Simulating a user database (In a real application, this would be an actual database)
users_db = {}

def create_user(username, password):
    """Create a new user with hashed password"""
    if username in users_db:
        raise ValueError("Username already exists.")
    
    hashed_password = generate_password_hash(password)
    users_db[username] = {'password': hashed_password}
    print(f"User {username} created successfully!")

def authenticate_user(username, password):
    """Authenticate user using username and password"""
    if username not in users_db:
        raise ValueError("User not found.")
    
    user_data = users_db[username]
    if not check_password_hash(user_data['password'], password):
        raise ValueError("Incorrect password.")
    
    print(f"User {username} authenticated successfully!")
    return generate_token(username)

def generate_token(username):
    """Generate JWT token for authenticated user"""
    expiration_time = timedelta(hours=1)  # Token expires in 1 hour
    payload = {
        'sub': username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """Verify if the JWT token is valid"""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")
    
# Example usage
if __name__ == "__main__":
    # Create a user and authenticate
    create_user("john_doe", "password123")
    
    # Authenticate user and generate token
    token = authenticate_user("john_doe", "password123")
    print(f"Generated JWT token: {token}")

    # Verify token
    decoded_data = verify_token(token)
    print(f"Decoded JWT token: {decoded_data}")
