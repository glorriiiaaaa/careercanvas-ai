# app/utils/tokens.py
#
# WHY THIS FILE EXISTS:
# Generates and verifies secure, time-limited tokens for password reset
# AND email verification links. Using itsdangerous means we don't need
# extra database columns to track pending requests - the token itself
# is self-contained and cryptographically signed, so it cannot be tampered with.

from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_reset_token(email):
    """Creates a signed token encoding the user's email, for password reset."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')


def verify_reset_token(token, max_age_seconds=3600):
    """Decodes a password-reset token. Returns email if valid, else None."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=max_age_seconds)
    except Exception:
        return None
    return email


def generate_verification_token(email):
    """
    Creates a signed token encoding the user's email, for email verification.
    Uses a DIFFERENT salt than password reset - this ensures a verification
    token can never accidentally be reused to reset a password, even though
    both are generated with the same SECRET_KEY.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification-salt')


def verify_verification_token(token, max_age_seconds=86400):
    """
    Decodes an email-verification token. Returns email if valid, else None.
    Default expiry is 24 hours (86400 seconds) - longer than password reset,
    since verification is lower-stakes and people may not check their inbox
    immediately after signing up.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification-salt', max_age=max_age_seconds)
    except Exception:
        return None
    return email