# app/__init__.py
import os
from flask import Flask
from app.config import config_by_name
from app.extensions import db, login_manager, migrate, csrf


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.models import user
    from app.models import resume

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.resume_analyzer import resume_analyzer_bp
    app.register_blueprint(resume_analyzer_bp)

    return app