# app/models/project_recommendation.py
from datetime import datetime
from app.extensions import db


class ProjectRecommendation(db.Model):
    __tablename__ = "project_recommendations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    interests = db.Column(db.String(255), nullable=False)   # comma-separated interests entered
    projects = db.Column(db.JSON, nullable=False)
    # list of: {title, difficulty, timeline, required_skills, tech_stack, db_design, github_structure, resume_description}

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("project_recommendations", lazy=True))

    def __repr__(self):
        return f"<ProjectRecommendation user {self.user_id}>"
