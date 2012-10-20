
DEBUG = True
APP_NAME = "flask-mold"
TEST_VERBOSITY = 2

SQLALCHEMY_DATABASE_URI = "postgresql://demo:demo@localhost/demodb"

BLUEPRINTS = [
	"home",
]