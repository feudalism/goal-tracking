from config import config

import os
from flask import Flask

REL_DIR = os.path.dirname(__file__)

def create_app(config_name='default', config_obj=None):
	"""Creates a Flask app object and sets the database filepath.
		
	Returns:
		app	: Flask object
	"""
	app = Flask(config_name)
	app.root_path = REL_DIR
	
	if config_obj is None:
		config_obj = config[config_name]
	
	app.config.from_object(config_obj)
	config_obj.init_app(app)
	
	return app