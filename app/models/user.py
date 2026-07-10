# app/models/user.py
#
# WHY THIS FILE EXISTS:
# Defines the User table - the foundation almost every other module
# will reference (resumes, roadmaps, interviews, etc. all belong to a User).
# Also handles password hashing so plain-text passwords never touch the database.

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager


class User(db.Model, UserMixin):
    """
    Represents a registered user of CareerCanvas AI.

    UserMixin (from flask_login) provides default implementations of
    properties Flask-Login requires (is_authenticated, is_active,
    is_anonymous, get_id) - saves us from writing that boilerplate ourselves.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)

    # unique=True enforces at the DATABASE level that no two users share
    # an email - this is a stronger guarantee than only checking in Python,
    # since it protects against race conditions (two signups at the exact
    # same millisecond both passing a Python-only check).
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Stores the HASH, never the plain password. Length 255 comfortably
    # fits Werkzeug's hash output format.
    password_hash = db.Column(db.String(255), nullable=False)

    is_email_verified = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, plain_password):
        """
        Hashes the given plain-text password and stores the hash.
        Called during signup, and later during password reset.
        """
        self.password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        """
        Verifies a plain-text password against the stored hash.
        Called during login. Returns True/False - never exposes the hash itself.
        """
        return check_password_hash(self.password_hash, plain_password)

    def __repr__(self):
        # Developer-facing representation (e.g., shown in debugger/logs).
        # Deliberately excludes password_hash from ever being printed.
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login calls this on every request for a logged-in user to
    reload the User object from the ID stored in their session cookie.
    This is how Flask-Login turns "a session says user 7 is logged in"
    into an actual usable User object in your route code.
    """
    return db.session.get(User, int(user_id))