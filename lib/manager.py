import click

from flask import Flask

import config
from lib.app import create_app
from plugins.db import db
from lib.utils import blueprint_template
from lib.migration import Migration

app = create_app(Flask(config.APP_NAME))

@click.group()
def manage():
    pass

@click.command()
def test():
    """Run tests"""
    import unittest
    suite = unittest.TestLoader()\
                .discover("tests", pattern="*_test.py")
    unittest.TextTestRunner(verbosity=config.TEST_VERBOSITY).run(suite)

manage.add_command(test)

@click.group("migration", options_metavar="\b")
def migration():
    """Database migration"""
    pass

manage.add_command(migration)

@click.command("init", options_metavar="\b")
def migration_init():
    """Initialize database migration structure"""
    Migration(app).init()

migration.add_command(migration_init)


@click.command("create", options_metavar="\b")
@click.argument("name")
def migration_create(name):
    """Create a migration file"""
    Migration(app).migration(name)

migration.add_command(migration_create)

@click.command("up", options_metavar="\b")
def migration_up():
    """Run migration revision up"""
    Migration(app).migrate("up")

migration.add_command(migration_up)

@click.command("down", options_metavar="\b")
def migration_down():
    """Run migration revision down"""
    Migration(app).migrate("down")

migration.add_command(migration_down)

@click.command("blueprint", options_metavar="\b")
@click.argument("name")
@click.option("--path", default=None)
@click.option("--templates", default=None)
def blueprint(name, path, templates):
    """Create blueprint structure"""
    templates = templates or "templates"
    path = path or name
    blueprint_template(name, templates)

manage.add_command(blueprint)

@click.command("runserver")
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=5000)
def runserver(host, port):
    """Development server"""
    app.run(host, port)

manage.add_command(runserver)

@click.command()
def shell():
    """Python shell with app locales"""
    import code

    with app.test_request_context():
        code.interact(None, local=dict(app=app, db=db))

manage.add_command(shell)

