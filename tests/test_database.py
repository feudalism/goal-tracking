from context import *

import unittest

EMPTY_DB_FILEPATH = abs_path("test.db")
NONEMPTY_DB_FILEPATH = abs_path("test_nonempty.db")

class TestEmptyDatabase(unittest.TestCase):
	"""Tests the functionality of the GoalsDb class
		starting from an empty database."""
	
	def setUp(self):
		"""Instantiates a test database with an empty table."""
		self.filepath = EMPTY_DB_FILEPATH
		self.db = Database(self.filepath)		
	
	def test_create_db(self):
		"""Tests the creation of an empty database."""
		self.assertTrue(file_exists(self.filepath))
	
	def test_add_one_goal(self):
		"""Tests addition of a single goal to the database."""
		goal = Goal(goal="Have 1M in savings.", category="Finance")
		self.db.add_goal(goal)
		self.assertTrue(self.db.contains_goal(goal))
		
	def test_add_multiple_goals(self):
		"""Tests addition of multiple goals to the database."""		
		goaldata1 = Goal(goal="Have 1M in savings.", category="Finance")
		goaldata2 = Goal(goal="Graduate with 1.0 CGPA.", category="Uni")
		goaldata3 = Goal(goal="Be healthy.", category="Health")
		
		goals_to_add = [goaldata1, goaldata2, goaldata3]
		
		for g in goals_to_add:
			self.db.add_goal(g)
			self.assertTrue(self.db.contains_goal(g))
		
	def tearDown(self):
		"""Removes modified database."""
		del self.db
		remove_file(self.filepath)
			
class TestNonEmptyDatabase(unittest.TestCase):
	"""Tests the functionality of the GoalsDb class
		starting from a non-empty database."""
	
	@classmethod
	def setUpClass(self):
		"""Instantiates a pre-filled test database."""
		self.filepath = NONEMPTY_DB_FILEPATH
		make_backup(self.filepath)
		self.db = Database(self.filepath)
		
	def get_first_goal(self):
		"""Retrieves the first goal object from the database."""
		return self.db.query(Goal)[0]
		
	def test_get_first_goal(self):
		"""Tests that the goal retrieval works."""
		print(self.get_first_goal())
		self.assertIsNotNone(self.get_first_goal())
		
	def test_add_duplicate_goal(self):
		"""Tests adding a duplicate goal to the database."""
		to_duplicate = self.get_first_goal()	
		duplicate = Goal(goal=to_duplicate.goal, category="Random")
		
		self.db.add_goal(duplicate)
		self.assertTrue(self.db.contains_goal(duplicate))
		
	def test_query_category(self):
		"""Tests querying goals by category."""
		goal = self.get_first_goal()
		newgoal = Goal(goal="Random goal", category=goal.category)
		self.db.add_goal(newgoal)
		
		result = self.db.query_cat(goal.category)
		self.assertIsNotNone(result)
	
	@classmethod
	def tearDownClass(self):
		"""Resets the non-empty database."""
		restore_backup(self.filepath)

	
if __name__ == '__main__':
	suite = unittest.TestSuite()
	addtests(suite, TestEmptyDatabase)
	addtests(suite, TestNonEmptyDatabase)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)