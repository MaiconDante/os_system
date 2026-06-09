from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# Import the Config class to load configurations
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Import models to ensure they are registered with SQLAlchemy
from app.models.client_model import Client
from app.models.order_service_model import OrderService
from app.models.user_model import User

# Factory function to create the Flask application
def create_app():
    app = Flask(__name__)
    # Load configurations from the Config class
    app.config.from_object(Config)
    # Initialize extensions with the app
    db.init_app(app)
    # Set up Flask-Login
    login_manager.init_app(app)
    # Set the login view for Flask-Login
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)
    # Register blueprints
    from app.routes.main_routes import main_bp
    from app.routes.clients_routes import client_bp
    from app.routes.order_service_routes import order_service_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.auth_routes import auth_bp
    # Register the main blueprint with the Flask app
    app.register_blueprint(main_bp)
    # Register the client blueprint with the Flask app
    app.register_blueprint(client_bp)
    # Register the order service blueprint with the Flask app
    app.register_blueprint(order_service_bp)
    # Register the dashboard blueprint with the Flask app
    app.register_blueprint(dashboard_bp)
    # Register the auth blueprint with the Flask app
    app.register_blueprint(auth_bp)

    return app

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )
