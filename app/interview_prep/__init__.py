# app/interview_prep/__init__.py
from flask import Blueprint

interview_prep_bp = Blueprint("interview_prep", __name__, url_prefix="/interview-prep")

from app.interview_prep import routes
