from context import *

import unittest
import os

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
		# Variables
		name = "goals"
		self.filepath = os.path.join(REL_DIR, "test.db")
		
		# Pre
		remove_file(self.filepath)
		self.db = GoalsDb(name, self.filepath)
	
	def test_create_db(self):
		"""
		Tests the creation of an empty database.
		"""
		self.assertTrue(file_exists(self.filepath))
		
	def test_add_one_goal(self):
		"""
		Tests addition of a single goal to the database.
		"""
		goal = "Have 1M in savings."
		goaldata = (goal, "Finance")
		self.db.add_goal(goaldata)
		
		self.assertTrue(self.db.is_contains_goal(goal))
		
	def test_add_multiple_goals(self):
		"""
		Tests addition of multiple goals to the database.
		"""
		goal1 = "Have 1M in savings."
		goal2 = "Have 2M in savings."
		goal3 = "Eat healthier."
		goaldata1 = (goal1, "Finance")
		goaldata2 = (goal2, "Finance")
		goaldata3 = (goal3, "Health")
		
		goals_to_add = [goaldata1, goaldata2, goaldata3]
		self.db.add_goal(goals_to_add)
		
		self.assertTrue(self.db.is_contains_goal(goal2))
		
class TestNonEmptyDatabase(unittest.TestCase):
	"""
	Tests the functionality of the GoalsDb class
	starting from a non-empty database.
	"""
	
	@classmethod
	def setUpClass(self):
		"""
		Instantiates a test database with an empty table.
		Any existing test databases are removed before creation
		of the new database.
		"""
		# Variables
		name = "goals"
		self.filepath = os.path.join(REL_DIR, "test_nonempty.db")
		
		# Pre
		make_backup(self.filepath)
		self.db = GoalsDb(name, self.filepath)
		
	def get_first_goaldata(self):
		query = f"SELECT * FROM {self.db.name} LIMIT 1"
		self.db.cursor.execute(query)
		return self.db.cursor.fetchone()
		
	def test_get_first_goaldata(self):
		self.assertIsNotNone(self.get_first_goaldata())
		
	def test_add_duplicate_goal(self):
		duplicate_data = self.get_first_goaldata()
		goal, cat, _ = duplicate_data
		
		self.db.add_goal((goal, cat))
		self.assertTrue(self.db.is_contains_goal(goal))
		
	def test_query_category(self):
		_, category, _ = self.get_first_goaldata()
		
		result = self.db.query_cat(category)
		self.assertIsNotNone(result)
	
		
	@classmethod
	def tearDownClass(self):
		"""
		Resets the non-empty database.
		"""
		restore_backup(self.filepath)


class TestTasks(TestNonEmptyDatabase):
	"""
	Tests the functionality of the Tasks class,
	using a non-empty database as a starting point.
	"""
	
	@classmethod
	def setUpClass(self):
		super().setUpClass()	
		
	def test_define_task(self):
		goal, category, _ = self.get_first_goaldata()
		task = Tasks(goal)
		t1 = task.add("Start saving up.")
		t2 = task.add("Invest.")
		
		t11 = task.add("Don't buy sweets.", parent=t1)
		
		print()
		task.print()
		
	@classmethod
	def tearDownClass(self):
		super().tearDownClass()
	
		
		
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestEmptyDatabase)
	addtests(suite, TestNonEmptyDatabase)
	addtests(suite, TestTasks)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)