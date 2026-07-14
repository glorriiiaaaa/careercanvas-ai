# app/roadmap/__init__.py
from flask import Blueprint

roadmap_bp = Blueprint('roadmap', __name__, url_prefix='/roadmap')

from app.roadmap import routes
