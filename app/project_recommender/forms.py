# app/project_recommender/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class InterestsForm(FlaskForm):
    interests = StringField(
        "Your Interests / Skills (comma-separated)",
        validators=[DataRequired(), Length(min=3, max=255)]
    )
    submit = SubmitField("Get Project Ideas")
