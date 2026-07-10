# app/extensions.py
#
# WHY THIS FILE EXISTS:
# Flask extensions (SQLAlchemy, LoginManager, Migrate, CSRFProtect) need to be
# created as objects, but NOT attached to a specific Flask app until create_app() runs.
#
# By defining them here as bare objects, any other file in the project
# (models, routes, forms, services) can safely do `from app.extensions import db`
# without triggering circular imports with app/__init__.py.
#
# The actual "wiring up" happens later in app/__init__.py via db.init_app(app)

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

# Database ORM instance - not yet bound to any app
db = SQLAlchemy()

# Handles user session management (login/logout state)
login_manager = LoginManager()

# Tracks database schema changes over time (like Git, but for DB structure)
migrate = Migrate()

# Protects ALL forms in the app from Cross-Site Request Forgery attacks automatically
csrf = CSRFProtect()