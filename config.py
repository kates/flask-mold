
DEBUG = True
APP_NAME = "flask-mold"
TEST_VERBOSITY = 2

SQLALCHEMY_DATABASE_URI = "sqlite:///demo.db"
TEST_DB_URI = "sqlite:///test.db" # if you want to run tests

SECRET_KEY = "this is my secret key"

BLUEPRINTS = [
    #('blueprint', '/mountpoint'),
    #("home", "/"),
    #("users", "/users"),
    ]

PLUGINS = [
    'db',
    ]
