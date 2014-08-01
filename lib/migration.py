import subprocess
import os
import sys
import logging

import alembic
from alembic.config import Config
from lib.utils import replace_alembic_env

class Migration(object):
    def __init__(self, app):
        config = None

        if app.config.get('TESTING'):
            config = Config()
            config.set_main_option('script_location', 'alembic')
            config.set_main_option('sqlalchemy.url', app.config.get('TEST_DB_URI'))
        else:
            config = Config(
                    os.path.realpath(os.path.dirname(__name__)) + "/alembic.ini")
            config.set_main_option('sqlalchemy.url', app.config.get('SQLALCHEMY_DATABASE_URI'))
        self.alembic_config = config

    def init(self):
        """Initialize alembic structure"""
        subprocess.call(['alembic', 'init', 'alembic'])
        replace_alembic_env()

    def migration(self, message):
        """Create migration file"""
        alembic.command.revision(self.alembic_config, message=message)

    def migrate(self, direction):
        """Migrate db revision"""
        if direction == 'up':
            alembic.command.upgrade(self.alembic_config, 'head')
        elif direction == 'down':
            alembic.command.downgrade(self.alembic_config, '-1')
        elif direction == 'base':
            alembic.command.downgrade(self.alembic_config, 'base')
        elif int(direction) == 0:
            alembic.command.downgrade(self.alembic_config, 'base')
        elif int(direction) > 0:
            alembic.command.upgrade(self.alembic_config, direction)
        elif int(direction) < 0:
            alembic.command.upgrade(self.alembic_config, direction)

