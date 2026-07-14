# app/resume_analyzer/__init__.py
from flask import Blueprint

resume_analyzer_bp = Blueprint('resume_analyzer', __name__, url_prefix='/resume-analyzer')

from app.resume_analyzer import routes
