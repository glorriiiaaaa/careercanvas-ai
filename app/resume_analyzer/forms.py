# app/resume_analyzer/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class ResumeUploadForm(FlaskForm):
    resume_file = FileField(
        "Upload Resume (PDF)",
        validators=[FileRequired(message="Please select a PDF file."), FileAllowed(["pdf"], "PDF files only.")]
    )
    submit = SubmitField("Analyze Resume")
