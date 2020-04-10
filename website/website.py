from context import *
from paths import DB_FILEPATH

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialise app
def init_app(filepath = DB_FILEPATH):
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_FILEPATH
	db = SQLAlchemy(app)
		
	app.run(debug=True)