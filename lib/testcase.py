from flask import Flask
import flask.ext.testing as testing
from lib.app import create_app
from lib.migration import Migration

import config

class TestCaseDBException(BaseException):
    pass

class TestCase(testing.TestCase):
    def create_app(self):
        app = Flask(config.APP_NAME)
        app = create_app(app)
        app.config["TESTING"] = True

        if app.config.get('TEST_DB_URI') is None:
            raise TestCaseDBException("No TEST_DB_URI specified in config.py!")

        app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('TEST_DB_URI')
        self.migration = Migration(app)
        return app

    def setUp(self):
        self.migration.migrate('up')

    def tearDown(self):
        self.migration.migrate('base')
