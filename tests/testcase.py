from flask import Flask
import flask.ext.testing as testing
from app import create_app

import config

class TestCase(testing.TestCase):
    def create_app(self):
        app = Flask(config.APP_NAME)
        app.config["TESTING"] = True
        return create_app(app)
