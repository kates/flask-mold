from flask import Blueprint
from flask import render_template
from flask import abort
from flask import request
from flask import redirect
from flask import url_for

from plugins.db import db

view = Blueprint("{{ name }}", __name__, template_folder="{{ templates }}")

@view.route("/")
def index():
    return render_template("index.html", title="{{ name }}")

