# app/interview_prep/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

CATEGORY_CHOICES = [
    ("HR", "HR Questions"),
    ("Technical", "Technical Questions"),
    ("Resume-Based", "Resume-Based Questions"),
]


class CategoryForm(FlaskForm):
    category = SelectField("Question Category", choices=CATEGORY_CHOICES, validators=[DataRequired()])
    submit = SubmitField("Start Practice Session")


class AnswerForm(FlaskForm):
    answer = TextAreaField("Your Answer", validators=[DataRequired()])
    submit = SubmitField("Submit Answer")
