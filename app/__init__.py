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
    from app.models import roadmap
    from app.models import interview
    from app.models import project_recommendation
    from app.models import skill
    from app.models import application
    from app.models import chat_message

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.resume_analyzer import resume_analyzer_bp
    app.register_blueprint(resume_analyzer_bp)

    from app.roadmap import roadmap_bp
    app.register_blueprint(roadmap_bp)

    from app.interview_prep import interview_prep_bp
    app.register_blueprint(interview_prep_bp)

    from app.project_recommender import project_recommender_bp
    app.register_blueprint(project_recommender_bp)

    from app.skill_tracker import skill_tracker_bp
    app.register_blueprint(skill_tracker_bp)

    from app.analytics import analytics_bp
    app.register_blueprint(analytics_bp)

    from app.ai_coach import ai_coach_bp
    app.register_blueprint(ai_coach_bp)

    return app