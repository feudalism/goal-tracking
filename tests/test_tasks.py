from context import *

import unittest
import datetime

TASKS_FILEPATH = abs_path("test_tasks.db")

class TestTasks(unittest.TestCase):
	"""Tests the functionality of the Tasks and TaskTree classes,
		using a non-empty database as a starting point."""
	
	@classmethod 
	def setUpClass(self):
		"""Initialises database for testing tasks."""
		self.filepath = TASKS_FILEPATH
		make_backup(self.filepath)
		self.db = Database(self.filepath)
		
	def gen_tree(self, goal):
		"""Generates the task tree for a given goal."""
		tasks = self.db.get_children(goal)
		return TaskTree(tasks, goal, do_print=True)
		
	def test_add_task(self):
		"""Tests adding a tasks to a goal."""
		g_1m = self.db.query_goal_id(1)
		g_study = self.db.query_goal_id(2)
		
		date = datetime.date(2030, 1, 1)
		
		t_spend = self.db.add_task("Spend less.", g_1m, deadline=date)
		t_cook = self.db.add_task("Invest.", g_1m)
		t_study = self.db.add_task("Study for DSV exam.", g_study)
		
		self.assertTrue(self.db.contains_task(t_spend))
		self.assertTrue(self.db.contains_task(t_cook))
		self.assertTrue(self.db.contains_task(t_study))
		
	def test_add_subtasks(self):
		"""Tests adding subtasks to a parent task."""
		task1 = self.db.query_task_id(1)
		
		t_netflix = self.db.add_task("Cancel Netflix.", task1)
		t_dropbox = self.db.add_task("Cancel Dropbox.", task1)
		tt_dropbox = self.db.add_task("Check when subscription ends.", t_dropbox)
		
		self.assertTrue(self.db.contains_task(t_netflix))
		self.assertTrue(self.db.contains_task(t_dropbox))
		self.assertTrue(self.db.contains_task(tt_dropbox))
		
	def test_print_tasktree(self):
		"""Tests functionality of the TaskTree class."""
		goal = self.db.query_goal_id(1)
		tree = self.gen_tree(goal)
		
		self.assertIsNotNone(tree)
		
	def test_tree_to_dict(self):
		"""Tests converting the task tree to an ordered dict."""
		goal = self.db.query_goal_id(1)
		tree = self.gen_tree(goal)
		d = tree.to_dict()
		self.assertIsNotNone(d)
		
	@classmethod
	def tearDownClass(self):
		"""Resets the non-empty database."""
		restore_backup(self.filepath)
		
		
if __name__ == '__main__':
	suite = unittest.TestSuite()
	addtests(suite, TestTasks)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)