# app/auth/routes.py
#
# WHY THIS FILE EXISTS:
# Contains the actual view functions (routes) for authentication.

from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.auth.forms import SignupForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
from app.models.user import User
from app.extensions import db
from app.utils.tokens import (
    generate_reset_token, verify_reset_token,
    generate_verification_token, verify_verification_token
)


def send_verification_email(user):
    token = generate_verification_token(user.email)
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    message = f'\n\n=== EMAIL VERIFICATION LINK (dev only) ===\n{verify_url}\n============================================\n'
    current_app.logger.info(message)
    print(message)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        new_user = User(
            full_name=form.full_name.data.strip(),
            email=form.email.data.lower().strip(),
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(new_user)

        flash('Account created! Please check the console for a verification link (dev mode), then log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)


@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    email = verify_verification_token(token)

    if email is None:
        flash('That verification link is invalid or has expired.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('That verification link is invalid or has expired.', 'error')
        return redirect(url_for('auth.login'))

    if user.is_email_verified:
        flash('Your email is already verified. You can log in.', 'info')
    else:
        user.is_email_verified = True
        db.session.commit()
        flash('Your email has been verified! You can now log in.', 'success')

    return redirect(url_for('auth.login'))


@auth_bp.route('/resend-verification', methods=['GET', 'POST'])
@login_required
def resend_verification():
    if current_user.is_email_verified:
        flash('Your email is already verified.', 'info')
    else:
        send_verification_email(current_user)
        flash('A new verification link has been sent (check the console in dev mode).', 'success')

    return redirect(url_for('auth.profile'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()

        if user:
            token = generate_reset_token(user.email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            message = f'\n\n=== PASSWORD RESET LINK (dev only) ===\n{reset_url}\n=======================================\n'
            current_app.logger.info(message)
            print(message)

        flash('If an account with that email exists, a reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)

    if email is None:
        flash('That reset link is invalid or has expired. Please request a new one.', 'error')
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('That reset link is invalid or has expired. Please request a new one.', 'error')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. Please log in with your new password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    The first genuinely protected page in the app. @login_required
    means Flask-Login automatically redirects anonymous visitors to
    the login page (configured earlier via login_manager.login_view).
    current_user is provided by Flask-Login - it's the logged-in
    User object, available in any route/template without us passing it manually.
    """
    form = ProfileForm(obj=current_user)  # pre-fills the form with existing data

    if form.validate_on_submit():
        current_user.full_name = form.full_name.data.strip()
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', form=form)