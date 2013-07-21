import os
import subprocess
import errno

from flask import Flask
from flask.ext.script import Manager, Shell

#from alembic import command
#from alembic.config import Config

import config
from app import create_app
from models import db
from lib.gunicorn_app import GunicornApp
from lib.utils import touch
from lib.utils import blueprint_template
from lib.migration import Migration


app = create_app(Flask(config.APP_NAME))
manager = Manager(app)

@manager.command
def server(port=5000):
    """Run gunicorn server"""
    options = {
        "bind": "0.0.0.0:%s" % port,
        "workers": 4,
        }
    gunicorn_app = GunicornApp(options, app)
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
    migration = Migration(app)
    migration.init()

@manager.command
def migrate(direction):
    """Migrate db revision"""
    migration = Migration(app)
    migration.migrate(direction)

@manager.command
def migration(message):
    """Create migration file"""
    migration = Migration(app)
    migration.migration(message)

@manager.command
def blueprint(name, path=None, templates=None):
    """create blueprint structure"""
    templates = templates or "templates"
    path = path or name
    blueprint_template(name, templates)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db)

