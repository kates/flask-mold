
DEBUG = True
APP_NAME = "flask-mold"
TEST_VERBOSITY = 2

SQLALCHEMY_DATABASE_URI = "sqlite:///demo.db"

BLUEPRINTS = [
	["home", "/"],
	["about", "/about"],
]
