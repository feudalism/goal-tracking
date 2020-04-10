import sqlite3
from itertools import compress

from models import *

class GoalsDb(object):
	"""
	Database of goals.
	"""
	
	def __init__(self, filepath):
		"""
		Creates an database file with an empty table,
		if the database at the filepath doesn't currently exist.
		Also creates a database session.
		"""
		self.filepath = filepath
		self.connection = sqlite3.connect(self.filepath)
		self.cursor = self.connection.cursor()
		
		self.session = self.get_session()
		
		self.create_table()
		self.save()
		print("Initialised database.")
		
	def __del__(self):
		"""
		Closes the cursor, connection and session
		before shutdown.
		"""
		self.cursor.close()
		self.connection.close()
		self.session.close()
		print("Database closed.")
		
	def get_session(self):
		"""
		Returns the database session.
		
		Returns: Session object
		"""
		URI = 'sqlite:///' + self.filepath
		engine = create_engine(URI, echo=False)	
		
		Session = sessionmaker(bind=engine)
		return Session()
	
	def save(self):
		"""
		Saves changes made to the database.
		"""
		self.session.commit()
		
	def create_table(self):
		"""
		Creates an empty table for a new database.
		"""
		query = f"""CREATE TABLE IF NOT EXISTS goals
			(id INTEGER PRIMARY KEY,
			goal TEXT,
			category TEXT,
			deadline DATETIME)"""
		self.cursor.execute(query)
		
		query = f"""CREATE TABLE IF NOT EXISTS tasks
			(id INTEGER PRIMARY KEY,
			task TEXT,
			deadline DATETIME,
			goal_id INTEGER,
			parent_id INTEGER,
			child_id INTEGER)"""
		self.cursor.execute(query)
		
	def add_goal(self, goal):
		"""
		Adds either a single row or multiple rows of data
		(goal object) to the database and saves.
		
		Params:	goal
				- Goal object of the goal to be added
				- Can either be a single goal object or a list
					of goal objects
		"""		
		
		# if self.is_duplicate(goal):
			# print("Duplicate.")
		# else:
		
		if isinstance(goal, list):
			self.add_multi_goal(goal)
		else:
			self.add_one_goal(goal)
		self.save()
			
	def add_one_goal(self, goal):
		"""
		Adds a single row of data
		(goal object) to the database if it is not a duplicate.
		
		Params:	Goal object of the goal to be added
		"""		
		if self.is_contains_goal(goal.goal):
			print("Duplicate.")
		else:
			self.session.add(goal)
			
	def add_multi_goal(self, goals):
		"""
		Adds a multiple rows of data
		(goal objects) to the database, filtering
		out duplicates.
		
		Params:	List of goal objects to be added
		"""		
		dupl_array = [self.is_contains_goal(g.goal) for g in goals]
		do_add = [not i for i in dupl_array]
		
		unique_goals = [g for i, g in enumerate(goals) if do_add[i]]		
		self.session.add_all(unique_goals)
	
	def add_task(self, task):
		"""Adds a task to the goal."""
		self.session.add(task)
		self.save()
		
	def add_task_to_goal(self, task, goal, deadline=None):
		task_obj = Task(task=task, goal=goal, deadline=deadline)
		self.add_task(task_obj)
		
		return task_obj
		
	def add_subtask_to_task(self, subtask, task, deadline=None):
		subtask_obj = Task(task=subtask,
					goal_id=task.goal_id,
					parent_id=task.id,
					deadline=deadline)
		self.add_task(subtask_obj)
		
		task.child_id = subtask_obj.id
		self.save()
		
		return subtask_obj
	
	def is_contains_goal(self, goal):
		"""
		Checks whether the goal is already within the database.
		
		Params:	goal	String of the goal to be added.

		Returns: True if goal is already in the database,
				 False otherwise.
		"""
		result = [g for g in self.session.query(Goal).\
				filter_by(goal=goal)]
		
		if result:
			return True
		else:
			return False
	
	def is_contains_task(self, task):
		"""
		Checks whether the task is already within the database.
		
		Params:	task	String of the task.

		Returns: True if task is already in the database,
				 False otherwise.
		"""
		result = [g for g in self.session.query(Task).\
				filter_by(task=task)]
		
		if result:
			return True
		else:
			return False
		
	def query_goal(self, goal):
		return self.session.query(Goal).filter_by(goal=goal)[0]
		
	def query_tasks_by_goal(self, goal):
		return [t for t in self.session.query(Task).\
						filter_by(goal_id=goal.id)]
						
	def query_tasks_by_parent(self, parent_id):
		return [t for t in self.session.query(Task).\
						filter_by(parent_id=parent_id)]
						
	def query_task_by_id(self, id):
		return [t for t in self.session.query(Task).\
						filter_by(id=id)]
	
	def query_cat(self, category):
		""""
		Queries the goals under the requested category.
		
		Params: 	category	Category string
		
		Returns:	List of goals in the database corresponding
					to the category.
		"""
		return [g.goal for g in self.session.query(Goal).\
				filter_by(category=category)]
	
