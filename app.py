from flask import Flask
from lib.app import create_app

if __name__ == "__main__":
    app = Flask(__name__)
    app = create_app(app)
    app.run()
