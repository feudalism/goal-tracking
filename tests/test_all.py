from context import *

import unittest
		
if __name__ == '__main__':
	suite = unittest.TestSuite()
	
	from test_database import *
	addtests(suite, TestEmptyDatabase)
	addtests(suite, TestNonEmptyDatabase)
	
	from test_tasks import *
	addtests(suite, TestTasks)
	
	from test_website import *
	addtests(suite, TestWebsite)
	
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)