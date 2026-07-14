# app/roadmap/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

CAREER_CHOICES = [
    ("Python Developer", "Python Developer"),
    ("Data Analyst", "Data Analyst"),
    ("Data Scientist", "Data Scientist"),
    ("Frontend Developer", "Frontend Developer"),
    ("Backend Developer", "Backend Developer"),
    ("Full Stack Developer", "Full Stack Developer"),
    ("AI Engineer", "AI Engineer"),
    ("Business Analyst", "Business Analyst"),
]


class RoadmapForm(FlaskForm):
    career_goal = SelectField("Select Career Goal", choices=CAREER_CHOICES, validators=[DataRequired()])
    submit = SubmitField("Generate Roadmap")
