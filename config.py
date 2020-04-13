from paths import TEST_FILEPATH
from paths import DB_FILEPATH

import flask_table # importing this resolves KeyError: 'babel' in website.routes when importing flask_table

import os

class Config:
	@staticmethod
	def init_app(app):
		with app.app_context():
			from db_setup import db
			from website import routes
			import models

			db.create_all()
			app.run()

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TEST_FILEPATH

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILEPATH
		
config = {
	'default': ProductionConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
}