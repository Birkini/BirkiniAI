import os
import logging
from typing import Optional
from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, Blueprint
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, raw: str):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password_hash, raw)

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))

# Auth blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password required', 'error')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.signup'))

        user = User(username=username)
        user.password = password
        db.session.add(user)
        db.session.commit()

        logger.info(f"New user registered: {username}")
        flash('Signup successful, please log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            logger.info(f"User logged in: {username}")
            flash('Login successful', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f"User logged out: {username}")
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))

# Main blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY', 'change-me'),
        'SQLALCHEMY_DATABASE_URI': os.getenv(
            'DATABASE_URI', 'sqlite:///users.db'
        ),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Create DB tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    create_app().run(debug=debug)

