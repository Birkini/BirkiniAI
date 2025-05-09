from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birkini.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the user schema (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Define the transaction schema (table)
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', back_populates='transactions')

User.transactions = db.relationship('Transaction', order_by=Transaction.id, back_populates='user')

# Function to create the tables in the database
def create_tables():
    """Create the necessary tables in the database."""
    with app.app_context():
        try:
            db.create_all()  # This will create all tables defined in the schema
            print("Tables created successfully!")
        except IntegrityError as e:
            print(f"Error creating tables: {e}")

# Function to add a new user
def add_user(username, email):
    """Add a new user to the database."""
    with app.app_context():
        new_user = User(username=username, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            print(f"User {username} added successfully!")
        except IntegrityError as e:
            print(f"Error adding user: {e}")

# Function to add a new transaction
def add_transaction(user_id, amount):
    """Add a new transaction for a user."""
    with app.app_context():
        new_transaction = Transaction(user_id=user_id, amount=amount)
        try:
            db.session.add(new_transaction)
            db.session.commit()
            print(f"Transaction of {amount} added for user ID {user_id} successfully!")
        except IntegrityError as e:
            print(f"Error adding transaction: {e}")

# Example usage
if __name__ == "__main__":
    # Create the tables if they don't exist
    create_tables()

    # Add a user to the database
    add_user('Alice', 'alice@example.com')

    # Add a transaction for the user
    add_transaction(1, 100.00)
