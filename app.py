import os
import logging

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_mail import Mail # Added this line

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Initialize CSRF protection
csrf = CSRFProtect()

# Initialize mail
mail = Mail() # Added this line

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "aaganshiksha_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///aaganshiksha.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["WTF_CSRF_ENABLED"] = True

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'aaganshiksha-noreply@example.com')
app.config['MAIL_DEBUG'] = True  # Enable to see detailed mail errors


# Initialize database
db.init_app(app)
mail.init_app(app) # Added this line

# Initialize CSRF protection
csrf.init_app(app)

# Make csrf_token available to all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Import user model for login_manager
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints after models are imported
with app.app_context():
    # Import models to create tables
    import models

    # Create database tables
    db.create_all()

    # Import and register blueprints
    from routes.home import home_bp
    from routes.admin import admin_bp
    from routes.teacher import teacher_bp
    from routes.auth import auth_bp
    from routes.attendance import attendance_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')

# Main execution
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)