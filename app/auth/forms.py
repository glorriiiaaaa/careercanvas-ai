# app/auth/forms.py
#
# WHY THIS FILE EXISTS:
# Defines form structure AND server-side validation rules in one place.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class SignupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Create Account')

    def validate_email(self, field):
        existing_user = User.query.filter_by(email=field.data.lower()).first()
        if existing_user:
            raise ValidationError('An account with this email already exists. Try logging in instead.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters.')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Reset Password')


class ProfileForm(FlaskForm):
    """
    Lets a logged-in user update their display name. Email is
    intentionally excluded here - changing email is a more sensitive
    operation (would need re-verification) and belongs in Settings
    later, not bundled into a simple profile edit.
    """
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    submit = SubmitField('Save Changes')