from context import *

import unittest
import shutil
import datetime

TASKS_FILEPATH = abs_path("test_tasks.db")
WEBSITE_DB = abs_path("test_website.db")

class TestTasks(unittest.TestCase):
	"""Tests the functionality of the Tasks class,
		using a non-empty database as a starting point.
	"""
	
	@classmethod 
	def setUpClass(self):
		self.filepath = TASKS_FILEPATH
		
		make_backup(self.filepath)
		self.db = GoalsDb(self.filepath)
		
	def get_goal(self, id=1):
		"""
		Retrieves the first goal object from the database.
		
		Returns:	First goal object from the database.
		"""
		return self.db.session.query(Goal)[id-1]
		
	def get_task(self, id=1):
		"""
		Retrieves the first task object from the database.
		
		Returns:	First goal object from the database.
		"""
		return self.db.session.query(Task)[id-1]
		
	def test_add_task(self):
		g_1m = self.get_goal(1)
		g_study = self.get_goal(2)
		
		date = datetime.date(2030, 1, 1)
		t_spend = "Spend less."
		t_cook = "Cook more."
		t_study = "Study for DSV exam."
		
		self.db.add_task_to_goal(t_spend, g_1m, deadline=date)
		self.db.add_task_to_goal(t_cook, g_1m)
		self.db.add_task_to_goal(t_study, g_study)
		
		self.assertTrue(self.db.is_contains_task(t_spend))
		self.assertTrue(self.db.is_contains_task(t_cook))
		self.assertTrue(self.db.is_contains_task(t_study))
		
	def test_add_subtasks(self):
		task1 = self.get_task(1)
		task2 = self.get_task(2)
		
		t_hulu = "Cancel Hulu."
		tt_hulu = "Check when Hu. subscription ends."
		t_netflix = "Cancel Netflix."
		t_dropbox = "Cancel Dropbox."
		tt_dropbox = "Check when subscription ends."
		
		hulu_tobj = self.db.add_subtask_to_task(t_hulu, task1)
		self.db.add_subtask_to_task(tt_hulu, hulu_tobj)
		self.db.add_subtask_to_task(t_netflix, task1)
		dropbox_tobj = self.db.add_subtask_to_task(t_dropbox, task1)
		self.db.add_subtask_to_task(tt_dropbox, dropbox_tobj)
		
		self.assertTrue(self.db.is_contains_task(t_hulu))
		self.assertTrue(self.db.is_contains_task(tt_hulu))
		self.assertTrue(self.db.is_contains_task(t_netflix))
		self.assertTrue(self.db.is_contains_task(t_dropbox))
		self.assertTrue(self.db.is_contains_task(tt_dropbox))
		
	def test_print_tasktree(self):
		random_goal = self.get_goal(1)
		tasks = self.db.query_tasks_by_goal(random_goal)
		tt = TaskTree(tasks)
		
	@classmethod
	def tearDownClass(self):
		"""
		Resets the non-empty database.
		"""
		shutil.copy(self.filepath, WEBSITE_DB)
		restore_backup(self.filepath)
		
		
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestTasks)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)