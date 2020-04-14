from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

app = Flask(__name__)

# test = os.environ["MOVIE_API_KEY"]

API_KEY="9053d7a271b82cb65b299800e362be0f"

# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_dash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "LOL"

bcrypt = Bcrypt(app)

# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)