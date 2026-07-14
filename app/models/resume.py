# app/models/resume.py
#
# WHY THIS FILE EXISTS:
# Stores each resume analysis a user runs. One user can have many
# analyses over time (e.g. re-uploading an improved resume) - hence
# the foreign key to User rather than fields living directly on User.

from datetime import datetime
from app.extensions import db


class ResumeAnalysis(db.Model):
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    original_filename = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)

    ats_score = db.Column(db.Integer, nullable=False)
    strengths = db.Column(db.JSON, nullable=False)       # list of strings
    weaknesses = db.Column(db.JSON, nullable=False)       # list of strings
    missing_skills = db.Column(db.JSON, nullable=False)   # list of strings
    keyword_suggestions = db.Column(db.JSON, nullable=False)  # list of strings
    improved_bullets = db.Column(db.JSON, nullable=False)     # list of {original, improved}

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Lets us write current_user.resume_analyses to get all analyses for a user
    user = db.relationship('User', backref=db.backref('resume_analyses', lazy=True))

    def __repr__(self):
        return f'<ResumeAnalysis {self.original_filename} - user {self.user_id}>'
