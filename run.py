# run.py
#
# WHY THIS FILE EXISTS:
# This is the single command you run to start the development server.
# It's kept separate from app/__init__.py so that "building" the app
# (the factory) and "running" the app (this file) are distinct concerns -
# useful later when tests import create_app() without ever starting a server.

from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True is fine here because DevelopmentConfig already sets DEBUG=True
    # via app.config - this app.run() call just starts the actual dev server.
    app.run(debug=app.config['DEBUG'])