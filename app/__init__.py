from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Import the Config class to load configurations
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Import models to ensure they are registered with SQLAlchemy
from app.models.client_model import Client

# Factory function to create the Flask application
def create_app():
    app = Flask(__name__)
    # Load configurations from the Config class
    app.config.from_object(Config)
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    # Register blueprints
    from app.routes.main_routes import main_bp
    from app.routes.clients_routes import client_bp
    # Register the main blueprint with the Flask app
    app.register_blueprint(main_bp)
    # Register the client blueprint with the Flask app
    app.register_blueprint(client_bp)

    return app
