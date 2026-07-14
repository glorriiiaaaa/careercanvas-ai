# app/models/roadmap.py
#
# WHY THIS FILE EXISTS:
# Stores a user's generated career roadmap. One user can regenerate/have
# multiple roadmaps over time (e.g. changing career goals), hence a
# foreign key to User rather than fields on User directly.

from datetime import datetime
from app.extensions import db


class Roadmap(db.Model):
    __tablename__ = 'roadmaps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    career_goal = db.Column(db.String(100), nullable=False)
    estimated_timeline = db.Column(db.String(50), nullable=False)   # e.g. "4-6 months"
    weekly_plan = db.Column(db.JSON, nullable=False)                # list of {week, focus, topics}
    recommended_courses = db.Column(db.JSON, nullable=False)         # list of strings
    suggested_projects = db.Column(db.JSON, nullable=False)          # list of strings

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('roadmaps', lazy=True))

    def __repr__(self):
        return f'<Roadmap {self.career_goal} - user {self.user_id}>'
