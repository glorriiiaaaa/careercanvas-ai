# app/auth/forms.py
#
# WHY THIS FILE EXISTS:
# Defines form structure AND server-side validation rules in one place.
# Flask-WTF renders these as HTML fields in templates, and validates
# submitted data server-side - never trust client-side validation alone.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class SignupForm(FlaskForm):
    """
    Registration form. Validators run automatically when we call
    form.validate_on_submit() in the route - if any fail, form.errors
    gets populated and we re-render the form with messages.
    """
    full_name = StringField(
        'Full Name',
        validators=[DataRequired(), Length(min=2, max=120)]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=120)]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters.')]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )

    submit = SubmitField('Create Account')

    def validate_email(self, field):
        """
        Custom validator - WTForms automatically calls any method named
        validate_<fieldname>. This checks the database for an existing
        user with this email BEFORE we attempt to insert a duplicate,
        giving a friendly error instead of a raw database crash.
        """
        existing_user = User.query.filter_by(email=field.data.lower()).first()
        if existing_user:
            raise ValidationError('An account with this email already exists. Try logging in instead.')