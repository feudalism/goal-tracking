from context import *

import unittest
import os
import shutil
import datetime

TASKS_FILEPATH = "test_tasks.db"

class TestTasks(unittest.TestCase):
	"""Tests the functionality of the Tasks class,
		using a non-empty database as a starting point.
	"""
	
	@classmethod 
	def setUpClass(self):
		self.filepath = os.path.join(REL_DIR, TASKS_FILEPATH)
		self.db = GoalsDb(self.filepath)
		
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
		
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestTasks)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)