import os
import subprocess
import errno

from flask import Flask
from flask.ext.script import Manager, Shell

from alembic import command
from alembic.config import Config

import config
from app import create_app
from models import db
from lib.gunicorn_app import GunicornApp
from lib.utils import mkdir_p
from lib.utils import touch

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

@manager.command
def blueprint(name, path=None, template=None):
	"""create blueprint structure"""
	template = template or "templates"
	path = path or name
	mkdir_p("blueprints/%s/%s" % (name, template,))
	touch("blueprints/%s/__init__.py" % name)
	touch("blueprints/%s/blueprint.py" % name)

@manager.shell
def make_shell_context():
	return dict(app=create_app(app), db=db)

if __name__ == "__main__":
	manager.run()
