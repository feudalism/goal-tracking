from flask import Flask
	
# Initialise app

def init(filepath):
	"""Creates a Flask app object and sets the database filepath.
		Creates a database object.
		Imports the routes to be run on the app.
		
	Returns:
		app	: Flask object
		db	: SQLAlchemy database
	"""
	app = Flask(__name__)
	print("App instance.")
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + filepath
	
	return app