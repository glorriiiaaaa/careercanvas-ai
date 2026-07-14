# app/skill_tracker/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

LEVEL_CHOICES = [("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")]


class SkillForm(FlaskForm):
    name = StringField("Skill Name", validators=[DataRequired(), Length(min=2, max=100)])
    level = SelectField("Level", choices=LEVEL_CHOICES, validators=[DataRequired()])
    progress_percent = IntegerField("Progress %", validators=[DataRequired(), NumberRange(min=0, max=100)], default=0)
    learning_hours = IntegerField("Learning Hours Logged", validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit = SubmitField("Save Skill")
