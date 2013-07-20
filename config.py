
DEBUG = True
APP_NAME = "flask-mold"
TEST_VERBOSITY = 2

SQLALCHEMY_DATABASE_URI = "sqlite:///demo.db"

SECRET_KEY = "this is my secret key"

BLUEPRINTS = [
    # ("home", "/"),
    # ("users", "/users"),
    ]

PLUGINS = [
        # "flask_login"
        ]
