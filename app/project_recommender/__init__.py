# app/project_recommender/__init__.py
from flask import Blueprint

project_recommender_bp = Blueprint("project_recommender", __name__, url_prefix="/project-recommender")

from app.project_recommender import routes
