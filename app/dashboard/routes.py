# app/dashboard/routes.py
#
# WHY THIS FILE EXISTS:
# Displays the main dashboard after login. Currently uses placeholder
# data - as we build Resume Analyzer, Skill Tracker, etc., we will
# replace these hardcoded values with real database queries, without
# needing to restructure this route.

from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp


@dashboard_bp.route('/')
@login_required
def index():
    """
    Main dashboard. All data below is placeholder for now - each
    value will be replaced by a real query once its owning module
    (Resume Analyzer, Skill Tracker, Analytics, etc.) is built.
    """
    dashboard_data = {
        'resume_score': 72,
        'current_goal': 'Full Stack Developer',
        'applications_sent': 8,
        'interviews_scheduled': 2,
        'learning_hours_this_week': 6,
        'motivational_quote': "The expert in anything was once a beginner.",
        'ai_insight': "Your resume is missing measurable impact statements. Adding numbers to 2-3 bullet points could raise your ATS score significantly.",
        'recent_activity': [
            {'text': 'Completed "Python Basics" module', 'time': '2 hours ago'},
            {'text': 'Uploaded resume for analysis', 'time': '1 day ago'},
            {'text': 'Started Full Stack Developer roadmap', 'time': '3 days ago'},
        ],
    }
    return render_template('dashboard/index.html', data=dashboard_data)
