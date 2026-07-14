# app/models/interview.py
#
# WHY THIS FILE EXISTS:
# Stores each interview practice session - the questions asked,
# the user's answers, and AI feedback/scores for each.

from datetime import datetime
from app.extensions import db


class InterviewSession(db.Model):
    __tablename__ = "interview_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    category = db.Column(db.String(50), nullable=False)   # "HR", "Technical", "Resume-Based"
    questions_and_answers = db.Column(db.JSON, nullable=False)
    # list of: {question, answer, feedback, answer_rating, confidence_score, grammar_score}

    overall_score = db.Column(db.Integer, nullable=False)  # average across all Q&A in this session

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("interview_sessions", lazy=True))

    def __repr__(self):
        return f"<InterviewSession {self.category} - user {self.user_id}>"
