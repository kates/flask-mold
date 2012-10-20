from flask import Flask
from models import db

import config

def create_app(app):
	"""loop thru the blueprints declared in the config.py"""
	app.config.from_object(config)

	db.init_app(app)
	#db.create_all()

	for bp in config.BLUEPRINTS:
		module = __import__("blueprints.%s.blueprint" % bp)
		app.register_blueprint(getattr(module, bp).blueprint.view)
	return app

if __name__ == "__main__":
	app = Flask(__name__)
	app = create_app(app)
	app.run()