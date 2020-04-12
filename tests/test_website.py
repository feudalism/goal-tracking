from context import *

import unittest
import os
import shutil
import datetime

DB_FILEPATH = "test_tasks.db"

class TestWebsite(unittest.TestCase):
	"""Tests the functionality of the website.
	"""
	
	@classmethod 
	def setUpClass(self):
		self.filepath = os.path.join(REL_DIR, DB_FILEPATH)
		# self.db = GoalsDb(self.filepath)
		
	def test_web_launch(self):
		website.app.init(DB_FILEPATH)
		
		
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestWebsite)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)