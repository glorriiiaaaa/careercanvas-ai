# app/auth/__init__.py
#
# WHY THIS FILE EXISTS:
# Creates the Blueprint object that groups all authentication-related
# routes together. This gets imported and registered onto the main app
# inside app/__init__.py's create_app() function.
#
# url_prefix='/auth' means every route defined with @auth_bp.route(...)
# is automatically prefixed - e.g. @auth_bp.route('/signup') becomes
# the real URL /auth/signup. This keeps routes namespaced and avoids
# collisions with other Blueprints we'll add later (dashboard, etc.)

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Import routes AFTER creating auth_bp, so route decorators like
# @auth_bp.route(...) in routes.py have something to attach to.
# This import is placed at the bottom deliberately to avoid circular imports.
from app.auth import routes