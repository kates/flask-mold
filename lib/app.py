import config
from models import db

def create_app(app):
    """loop thru the blueprints declared in the config.py"""
    app.config.from_object(config)

    for plugin in config.PLUGINS:
        module = __import__("plugins.%s" % plugin)
        getattr(module, plugin).init_app(app)

    for bp, mount in config.BLUEPRINTS:
        module = __import__("blueprints.%s.%s_blueprint" % (bp, bp,))
        app.register_blueprint(getattr(getattr(module, bp), "%s_blueprint" % bp).view,
                url_prefix=mount)
    return app


