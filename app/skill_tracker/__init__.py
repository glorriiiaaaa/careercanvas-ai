# app/skill_tracker/__init__.py
from flask import Blueprint

skill_tracker_bp = Blueprint("skill_tracker", __name__, url_prefix="/skill-tracker")

from app.skill_tracker import routes
