# app/ai_coach/forms.py
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ChatForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField("Send")
