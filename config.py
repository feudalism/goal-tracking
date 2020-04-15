from paths import TEST_FILEPATH, DB_FILEPATH

import os
import flask_table
# importing flask_table resolves KeyError: 'babel' in website.routes when importing flask_table

class Config:
	"""Base class for app configuration."""
	
	@staticmethod
	def init_app(app):
		"""Loads necessary imports which require the app instance."""
		with app.app_context():
			from database.setup import db
			from website import routes
			from database import models

			db.create_all()

class TestingConfig(Config):
	"""App configuration for testing."""
	
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TEST_FILEPATH
	
	@staticmethod
	def init_app(app):
		"""Loads necessary imports which require the app instance.
			The app then run in debug mode."""
		Config.init_app(app)
		app.run(debug=True)

class ProductionConfig(Config):
	"""App configuration for normal usage."""
	
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILEPATH
	
	@staticmethod
	def init_app(app):
		"""Loads necessary imports which require the app instance.
			The app then run."""
		Config.init_app(app)
		app.run()
		
config = {
	'default': ProductionConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
}