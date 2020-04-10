from context import *

import unittest
import os
import shutil
import datetime

EMPTY_DB_FILEPATH = "test.db"
NONEMPTY_DB_FILEPATH = "test_nonempty.db"
TASKS_FILEPATH = "test_tasks.db"

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
		self.filepath = os.path.join(REL_DIR, EMPTY_DB_FILEPATH)
		
		# Pre
		remove_file(self.filepath)
		self.db = GoalsDb(self.filepath)	
	
	def test_create_db(self):
		"""
		Tests the creation of an empty database.
		"""
		self.assertTrue(file_exists(self.filepath))
		
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
		goal2 = "Have 2M in savings."
		goal3 = "Eat healthier."
		
		goaldata1 = Goal(goal=goal1, category="Finance")
		goaldata2 = Goal(goal=goal2, category="Finance")
		goaldata3 = Goal(goal=goal3, category="Health")
		
		goals_to_add = [goaldata1, goaldata2, goaldata3]
		self.db.add_goal(goals_to_add)
		
		self.assertTrue(self.db.is_contains_goal(goaldata2.goal))
		
		# Save for non-empty database
		shutil.copy(self.filepath, NONEMPTY_DB_FILEPATH)
		shutil.copy(self.filepath, TASKS_FILEPATH)
		
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
		self.filepath = os.path.join(REL_DIR, filepath)
		
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

class TestTasks(TestNonEmptyDatabase):
	"""
	Tests the functionality of the Tasks class,
	using a non-empty database as a starting point.
	"""
	
	@classmethod 
	def setUpClass(self):
		self.filepath = os.path.join(REL_DIR, TASKS_FILEPATH)
		self.db = GoalsDb(self.filepath)
		# pass
		# super().setUpClass(TASKS_FILEPATH)
		
	def get_first_task(self):
		"""
		Retrieves the first task object from the database.
		
		Returns:	First goal object from the database.
		"""
		return self.db.session.query(Task)[0]
		
	def test_add_task(self):
		random_goal = self.get_first_goal()
		
		date = datetime.date(2030, 1, 1)
		task1 = "Spend less."
		task2 = "Cook more."
		
		self.db.add_task_to_goal(task1, random_goal, deadline=date)
		self.db.add_task_to_goal(task2, random_goal)
		
		self.assertTrue(self.db.is_contains_task(task1))
		self.assertTrue(self.db.is_contains_task(task2))
		
	def test_add_subtasks(self):
		random_task = self.get_first_task()
		
		t_hulu = "Cancel Hulu."
		tt_hulu = "Check when Hu. subscription ends."
		t_dropbox = "Cancel Dropbox."
		tt_dropbox = "Check when subscription ends."
		
		t_hulu_obj = self.db.add_subtask_to_task(t_hulu, random_task)
		self.db.add_subtask_to_task("Cancel Netflix.", random_task)
		t_dropbox_obj = self.db.add_subtask_to_task(t_dropbox, random_task)
		
		self.db.add_subtask_to_task(tt_hulu, t_hulu_obj)
		self.db.add_subtask_to_task(tt_dropbox, t_dropbox_obj)
		
		self.assertTrue(self.db.is_contains_task(t_hulu))
		self.assertTrue(self.db.is_contains_task(tt_hulu))
		self.assertTrue(self.db.is_contains_task(t_dropbox))
		self.assertTrue(self.db.is_contains_task(tt_dropbox))
		
	def test_print_tasktree(self):
		random_goal = self.get_first_goal()
		tasks = self.db.query_tasks_by_goal(random_goal)
		tt = TaskTree(tasks)
		
	@classmethod
	def tearDownClass(self):
		pass
		# shutil.copy(self.filepath, "test_tasks_view.db")
		# super().tearDownClass()
	
		
		
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestEmptyDatabase)
	addtests(suite, TestNonEmptyDatabase)
	addtests(suite, TestTasks)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)