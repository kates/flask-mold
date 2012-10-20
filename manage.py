from flask import Flask
from flask.ext.script import Manager

import config
from app import create_app
from lib.gunicorn_app import GunicornApp

app = Flask(config.APP_NAME)
manager = Manager(app)

@manager.command
def server(port=5000):
	options = {
		"bind": "0.0.0.0:%s" % port,
		"workers": 4,
		}
	gunicorn_app = GunicornApp(options, create_app(app))
	gunicorn_app.run()


@manager.command
def test():
	"""run tests"""
	import unittest
	suite = unittest.TestLoader()\
				.discover("tests", pattern="*_test.py")
	unittest.TextTestRunner(verbosity=config.TEST_VERBOSITY).run(suite)


if __name__ == "__main__":
	manager.run()