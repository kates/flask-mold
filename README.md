# Flask-Mold #

**Flask Application Boilerplate**

Boilerplate codes to help getting started with [Flask](http://flask.pocoo.org) faster.
Batteries included. Manage database migration with [Alembic](http://pypi.python.org/pypi/alembic).


### Get Started ###

Get the source and setup the environment

	git clone https://github.com/kates/flask-mold.git
	cd flask-mold
	virtuanenv --distribute .venv
	source .venv/bin/activate
	pip install -r requirements.txt

Update config.py

	# in config.py

	SQLALCHEMY_DATABASE_URI = "postgresql://demo:demo@localhost/demodb"
	
Initialize alembic

	python manage.py migration init

Update the generated alembic.ini with the same db uri as in the config.py

	# in alembic.ini

	sqlalchemy.url = postgresql://demo:demo@localhost/demodb

Create migration file

	python manage.py migration create create_users

Edit the migration file created above

	# in XXXXXX_create_users.py

	"""create_users
	Revision ID: 71f880c1c35
	Revises: None
	Create Date: 2012-10-20 14:22:02.857840
	"""

	# revision identifiers, used by Alembic.
	revision = '71f880c1c35'
	down_revision = None

	from alembic import op
	import sqlalchemy as sa

	def upgrade():
	    op.create_table("users",
	    	sa.Column("id", sa.Integer, primary_key=True),
	    	sa.Column("name", sa.String(50), nullable=False),
	    	sa.Column("dept", sa.String(50)),
	    	)

	def downgrade():
	    op.drop_table("users")

Run the migration:

	python manage.py migration up

Update the models.py to reflect the db schema

	# in models.py

	class User(db.Model):
		__tablename__ = "users"

		id = db.Column("id", db.Integer, primary_key=True)
		name = db.Column("name", db.String(50), nullable=False)
		dept = db.Column("dept", db.String(10))

Create a blueprint inside blueprints with the following structure

	home
	├── __init__.py
	├── blueprint.py
	└── templates
	    └── index.html

by running the blueprint generator

	python manage.py blueprint home

Update the blueprint

	# in blueprints/home/home_blueprint.py

	from flask import Blueprint
	from flask import render_template
	from flask import abort
	from flask import request
	from flask import redirect
  from flask import url_for
	from plugins.db import db
	from models import User

	view = Blueprint("home", __name__, template_folder="templates")

	@view.route("/")
	def index():
		users = User.query.order_by("id desc").all()
		return render_template("index.html", users=users)

	@view.route("/create_user", methods=["POST"])
	def new_user():
		name = request.values.get("name")
		dept = request.values.get("dept")
		user = User()
		user.name = name
		user.dept = dept

		db.session.add(user)
		db.session.commit()

		return redirect("/")

Write the index.html
	
	# in blueprints/home/templates/index.html

	<h1>Home</h1>

	<ul>
		{% for user in users %}
		<li>{{ user.name }} - {{ user.dept }}</li>
		{% endfor %}
	</ul>

	<form method="POST" action="/create_user">
		<div>
			<label>Name: <input type="text" name="name" /></label>
		</div>

		<div>
			<label>Dept: <input type="text" name="dept" /></label>
		</div>

		<div>
			<input type="submit" value="Submit" />
		</div>
	 </form>

Run the server

	python manage.py runserver

Point your browser to http://localhost:5000

##### Plugins #####

TODO: Flask extensions can be used directly but code may be organized through plugins.


##### Shell #####

The manage.py script includes a shell command that you can use to quickly view
or manipulate your model.

Running

	python manage.py shell

will put you into the python shell with you application and db context loaded.

	>>> from models import User                    
	>>> user = User()                              
	>>> user.name = "John Doe"                     
	>>> user.dept = "Finance"                      
	>>> db.session.add(user)                       
	>>> db.session.commit()                        
	>>> users = User.query.all()                   
	>>> [[user.name, user.dept] for user in users] 
	[[u'John Doe', u'Finance']]                    

#### TODO ####

* Write guide to testing
