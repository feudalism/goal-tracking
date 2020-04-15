from context import *

import unittest

EMPTY_DB = abs_path("test_empty.db")
DB_FILEPATH = abs_path("test_website.db")

class TestWebsite(unittest.TestCase):
	"""Tests the functionality of the website."""
		
	def launch_app(self, db_filepath):
		"""Configures the app with the database given and launches it.
		
		Args:
			db_filepath	Absolute filepath of the database
		"""
		config = TestingConfig()
		config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_filepath
		self.app = create_app('', config)
		
	@unittest.skip("")
	def test_web_launch(self):
		"""Runs the app using an empty database."""
		self.launch_app(EMPTY_DB)
		
	def test_custom_config(self):
		"""Runs the app using a database pre-filled with goals and tasks"""
		self.launch_app(DB_FILEPATH)
		
		
if __name__ == '__main__':
	suite = unittest.TestSuite()
	addtests(suite, TestWebsite)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)