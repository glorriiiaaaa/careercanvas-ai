# app/auth/routes.py
#
# WHY THIS FILE EXISTS:
# Contains the actual view functions (routes) for authentication.
# Each function should stay focused on HTTP concerns (parsing requests,
# returning responses) - the "how do we create a user" logic itself
# is simple enough here to stay inline, but note: in more complex modules
# later (Resume Analyzer, AI Coach), we'll push logic into a services.py
# file instead of routes.py, keeping routes thin.

from flask import render_template, redirect, url_for, flash
from app.auth import auth_bp
from app.auth.forms import SignupForm
from app.models.user import User
from app.extensions import db


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles both displaying the signup form (GET) and processing
    a submitted signup form (POST). This GET+POST combo on one route
    is a standard Flask pattern - avoids duplicating the template
    rendering logic across two separate functions.
    """
    form = SignupForm()

    # validate_on_submit() is True only on a POST request where all
    # validators (including our custom validate_email) passed.
    if form.validate_on_submit():
        new_user = User(
            full_name=form.full_name.data.strip(),
            email=form.email.data.lower().strip(),
        )
        # set_password() hashes the password - defined on the User model.
        # The plain password from the form is never stored or logged anywhere.
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    # GET request, OR validation failed on POST - re-render the form.
    # WTForms automatically attaches error messages to form.<field>.errors,
    # which we'll display in the template.
    return render_template('auth/signup.html', form=form)