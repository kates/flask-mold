import config

def create_app(app):
	app.config.from_object(config)
	for bp in config.BLUEPRINTS:
		module = __import__("blueprints.%s.blueprint" % bp)
		app.register_blueprint(getattr(module, bp).blueprint.view)
	return app