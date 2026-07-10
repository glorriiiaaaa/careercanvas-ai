# app/__init__.py
#
# WHY THIS FILE EXISTS:
# This is the Application Factory - the single function responsible for
# building a fully configured Flask app instance. Nothing runs the app
# from here directly; that happens in run.py. Keeping "build" and "run"
# separate is what lets us create multiple app instances with different
# configs (e.g., one for tests, one for development) without conflict.

import os
from flask import Flask
from app.config import config_by_name
from app.extensions import db, login_manager, migrate, csrf


def create_app(config_name=None):
    """
    Factory function - builds and returns a configured Flask app.

    config_name: 'development' or 'production'. If not provided,
    we read it from the FLASK_ENV environment variable, defaulting
    to 'development' if that's also missing (safe default).
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)

    # Load the correct settings class (DevelopmentConfig or ProductionConfig)
    app.config.from_object(config_by_name[config_name])

    # Bind our previously-uninitialized extensions to THIS specific app instance.
    # This two-step pattern (create in extensions.py, bind here) is what
    # avoids circular imports as the project grows.
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Import models so SQLAlchemy/Flask-Migrate is aware of them.
    # Must happen AFTER db.init_app() to avoid circular import issues.
    from app.models import user

    # Register Blueprints - each module's routes get wired into the app here
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app