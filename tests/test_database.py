from context import *

import unittest
import shutil

EMPTY_DB_FILEPATH = abs_path("test.db")
NONEMPTY_DB_FILEPATH = abs_path("test_nonempty.db")
TASKS_FILEPATH = abs_path("test_tasks.db")

class TestEmptyDatabase(unittest.TestCase):
	"""
	Tests the functionality of the GoalsDb class
	starting from an empty database.
	"""
	
	def setUp(self):
		"""
		Instantiates a test database with an empty table.
		Any existing test databases are removed before creation
		of the new database.
		"""
		self.filepath = EMPTY_DB_FILEPATH
		self.db = GoalsDb(self.filepath)		
	
	def test_create_db(self):
		"""
		Tests the creation of an empty database.
		"""
		self.assertTrue(file_exists(self.filepath))
		
		# Save empty database
		shutil.copy(self.filepath, abs_path("test_empty.db"))
		
	def test_add_one_goal(self):
		"""
		Tests addition of a single goal to the database.
		"""
		goal = Goal(goal="Have 1M in savings.",
				category="Finance")
		print(goal)
		self.db.add_goal(goal)
		
		self.assertTrue(self.db.is_contains_goal(goal.goal))
		
	def test_add_multiple_goals(self):
		"""
		Tests addition of multiple goals to the database.
		"""
		goal1 = "Have 1M in savings."
		goal2 = "Graduate with 1.0 CGPA."
		goal3 = "Eat healthier."
		
		goaldata1 = Goal(goal=goal1, category="Finance")
		goaldata2 = Goal(goal=goal2, category="Uni")
		goaldata3 = Goal(goal=goal3, category="Health")
		
		goals_to_add = [goaldata1, goaldata2, goaldata3]
		self.db.add_goal(goals_to_add)
		
		self.assertTrue(self.db.is_contains_goal(goaldata2.goal))
		
		# Save for non-empty databases
		shutil.copy(self.filepath, NONEMPTY_DB_FILEPATH)
		shutil.copy(self.filepath, TASKS_FILEPATH)
		
	def tearDown(self):
		del self.db
		remove_file(self.filepath)
			
class TestNonEmptyDatabase(unittest.TestCase):
	"""
	Tests the functionality of the GoalsDb class
	starting from a non-empty database.
	"""
	
	@classmethod
	def setUpClass(self, filepath=NONEMPTY_DB_FILEPATH):
		"""
		Instantiates a test database with an empty table.
		Any existing test databases are removed before creation
		of the new database.
		"""
		# Variables
		self.filepath = filepath
		
		# Pre
		make_backup(self.filepath)
		self.db = GoalsDb(self.filepath)
		
	def get_first_goal(self):
		"""
		Retrieves the first goal object from the database.
		
		Returns:	First goal object from the database.
		"""
		return self.db.session.query(Goal)[0]
		
	def test_get_first_goal(self):
		"""
		Tests that the goal retrieval works.
		"""
		self.assertIsNotNone(self.get_first_goal())
		
	def test_add_duplicate_goal(self):
		"""
		Tests adding a duplicate goal to the database.
		"""
		to_duplicate = self.get_first_goal()		
		
		duplicate = Goal(goal=to_duplicate.goal,
						category="Random")
		self.db.add_goal(duplicate)
		self.assertTrue(self.db.is_contains_goal(duplicate.goal))
		
	def test_query_category(self):
		goal_obj = self.get_first_goal()
		result = self.db.query_cat(goal_obj.category)
		self.assertIsNotNone(result)
	
	@classmethod
	def tearDownClass(self):
		"""
		Resets the non-empty database.
		"""
		restore_backup(self.filepath)

	
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestEmptyDatabase)
	addtests(suite, TestNonEmptyDatabase)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)