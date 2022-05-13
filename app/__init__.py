from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from config import config

# Extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def init_app(config_name):
    app = Flask(__name__, instance_relative_config=False)

    # Set configurations
    app.config.from_object(config.get(config_name or 'default'))

    # Import models
    from app.models import user, user_invites, company, vehicle

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        # Import and register blueprints
        from app.auth import views as auth_views
        from app.api import views as api_views

        app.register_blueprint(auth_views.auth_bp)
        app.register_blueprint(api_views.api_bp)

        return app
