from config import config

from flask import Flask

def create_app(config_name, config_obj=None):
	"""Creates a Flask app object and sets the database filepath.
		
	Returns:
		app	: Flask object
	"""
	app = Flask(__name__)
	
	if config_obj is None:
		config_obj = config[config_name]
	
	app.config.from_object(config_obj)
	config_obj.init_app(app)
	
	return app