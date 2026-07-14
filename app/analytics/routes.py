# app/analytics/routes.py
#
# WHY THIS FILE EXISTS:
# Aggregates data across multiple modules (applications, interviews,
# skills, resume analyses) into summary statistics and chart-ready data.
# This route does NOT create new domain data itself (except applications,
# added here as a lightweight tracker) - it mostly reads and counts
# existing records from tables owned by other modules.

from datetime import datetime
from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.analytics import analytics_bp
from app.analytics.forms import ApplicationForm
from app.models.application import Application
from app.models.interview import InterviewSession
from app.models.skill import Skill
from app.models.resume import ResumeAnalysis
from app.extensions import db


@analytics_bp.route("/")
@login_required
def index():
    applications = Application.query.filter_by(user_id=current_user.id).all()
    interviews = InterviewSession.query.filter_by(user_id=current_user.id).all()
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    resumes = ResumeAnalysis.query.filter_by(user_id=current_user.id).all()

    status_counts = {"Applied": 0, "Interview": 0, "Offer": 0, "Rejected": 0}
    for app_row in applications:
        status_counts[app_row.status] = status_counts.get(app_row.status, 0) + 1

    total_learning_hours = sum(s.learning_hours for s in skills)

    summary = {
        "applications_sent": len(applications),
        "interviews_completed": len(interviews),
        "offers": status_counts["Offer"],
        "rejections": status_counts["Rejected"],
        "learning_hours": total_learning_hours,
        "resumes_analyzed": len(resumes),
        "skills_tracked": len(skills),
    }

    chart_data = {
        "status_labels": list(status_counts.keys()),
        "status_values": list(status_counts.values()),
    }

    recent_applications = (
        Application.query.filter_by(user_id=current_user.id)
        .order_by(Application.applied_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "analytics/index.html", summary=summary, chart_data=chart_data,
        recent_applications=recent_applications
    )


@analytics_bp.route("/applications/add", methods=["GET", "POST"])
@login_required
def add_application():
    form = ApplicationForm()

    if form.validate_on_submit():
        new_app = Application(
            user_id=current_user.id,
            company_name=form.company_name.data.strip(),
            role_title=form.role_title.data.strip(),
            status=form.status.data,
            applied_date=form.applied_date.data,
        )
        db.session.add(new_app)
        db.session.commit()
        flash(f"Added application for {new_app.role_title} at {new_app.company_name}.", "success")
        return redirect(url_for("analytics.index"))

    return render_template("analytics/add_application.html", form=form)
