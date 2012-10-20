from flask import Blueprint
from flask import render_template
from flask import abort


view = Blueprint("home", __name__, template_folder="templates")

@view.route("/")
def index():
	return render_template("index.html")