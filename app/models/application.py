# app/models/application.py
#
# WHY THIS FILE EXISTS:
# A lightweight model so Analytics has real job-application data to
# aggregate, rather than only placeholder numbers. Kept intentionally
# simple - a dedicated Job Application Tracker module could expand on
# this later without breaking Analytics, since Analytics just counts
# rows here by status.

from datetime import datetime
from app.extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    company_name = db.Column(db.String(150), nullable=False)
    role_title = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Applied")
    # status values: Applied, Interview, Offer, Rejected

    applied_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("applications", lazy=True))

    def __repr__(self):
        return f"<Application {self.company_name} - {self.status}>"
