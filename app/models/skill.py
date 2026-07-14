# app/models/skill.py
from datetime import datetime
from app.extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(20), nullable=False, default="Beginner")   # Beginner/Intermediate/Advanced
    progress_percent = db.Column(db.Integer, nullable=False, default=0)     # 0-100, user-set
    learning_hours = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("skills", lazy=True))

    def __repr__(self):
        return f"<Skill {self.name} - user {self.user_id}>"
