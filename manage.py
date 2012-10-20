import os
import subprocess

from flask import Flask
from flask.ext.script import Manager

from alembic import command
from alembic.config import Config

import config
from app import create_app
from lib.gunicorn_app import GunicornApp

alembic_config = Config(os.path.realpath(os.path.dirname(__name__)) + "/alembic.ini")

app = Flask(config.APP_NAME)
manager = Manager(app)

@manager.command
def server(port=5000):
	"""Run gunicorn server"""
	options = {
		"bind": "0.0.0.0:%s" % port,
		"workers": 4,
		}
	gunicorn_app = GunicornApp(options, create_app(app))
	gunicorn_app.run()


@manager.command
def test():
	"""Run tests"""
	import unittest
	suite = unittest.TestLoader()\
				.discover("tests", pattern="*_test.py")
	unittest.TextTestRunner(verbosity=config.TEST_VERBOSITY).run(suite)

@manager.command
def alembic():
	"""Initialize alembic"""
	subprocess.call(["alembic", "init", "alembic"])

@manager.command
def migrate(direction):
	"""Migrate db revision"""
	if direction == "up":
		command.upgrade(alembic_config, "head")
	elif direction == "down":
		command.downgrade(alembic_config, "-1")

@manager.command
def migration(message):
	"""Create migration file"""
	command.revision(alembic_config, message=message)


if __name__ == "__main__":
	manager.run()