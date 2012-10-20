from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# class User(db.Model):
# 	__tablename__ = "users"

# 	id = db.Column("id", db.Integer, primary_key=True)
# 	name = db.Column("name", db.String(50), nullable=False)
# 	dept = db.Column("dept", db.String(10))
