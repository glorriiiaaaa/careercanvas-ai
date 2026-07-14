# app/analytics/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

STATUS_CHOICES = [("Applied", "Applied"), ("Interview", "Interview"), ("Offer", "Offer"), ("Rejected", "Rejected")]


class ApplicationForm(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired(), Length(min=1, max=150)])
    role_title = StringField("Role Title", validators=[DataRequired(), Length(min=1, max=150)])
    status = SelectField("Status", choices=STATUS_CHOICES, validators=[DataRequired()])
    applied_date = DateField("Applied Date", validators=[DataRequired()])
    submit = SubmitField("Save Application")
