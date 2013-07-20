from gunicorn.app.base import Application

# stole this from somewhere i forgot the link

class GunicornApp(Application):
    def __init__(self, options={}, app=None):
        self.app = app
        self.usage = None
        self.callable = None
        self.options = options
        self.prog = None
        self.do_load_config()

    def init(self, *args):
        cfg = {}

        for k, v in self.options.items():
            kk = k.lower()
            if kk in self.cfg.settings and v is not None:
                cfg[kk] = v

        return cfg

    def load(self):
        return self.app
