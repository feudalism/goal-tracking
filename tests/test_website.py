from context import *

import unittest
import os
import shutil
import datetime

EMPTY_DB = abs_path("test_empty.db")
DB_FILEPATH = abs_path("test_website.db")

class TestWebsite(unittest.TestCase):
	"""Tests the functionality of the website.
	"""
	
	# @classmethod 
	# def setUpClass(self):
		# self.config_name = 'testing'		
		
	def launch_app(self, db_filepath):
		config = TestingConfig()
		config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_filepath
		self.app = create_app('', config)
		
	@unittest.skip("")
	def test_web_launch(self):
		self.launch_app(EMPTY_DB)
		
	def test_custom_config(self):
		self.launch_app(DB_FILEPATH)
		
		
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestWebsite)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)