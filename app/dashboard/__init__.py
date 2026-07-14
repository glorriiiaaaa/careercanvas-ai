# app/dashboard/__init__.py
#
# WHY THIS FILE EXISTS:
# Creates the Blueprint for the Dashboard module - the main landing
# page users see after logging in.

from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from app.dashboard import routes
