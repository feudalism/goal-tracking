from .creator import *

from sqlalchemy.orm import sessionmaker

class Database(object):
	"""Class representing the database of goals/tasks
		and some associated convenience functions."""
	
	def __init__(self, filepath):
		"""Creates an database file with an empty table,
			if the database at the filepath doesn't currently exist.
			Also creates a database session."""
		self.filepath = filepath
		self.session = self.__get_session()
		
		create_tables(self.filepath)
		self.save()
		print("Initialised database.")
		
	def __del__(self):
		"""Closes the session before shutdown."""
		self.session.close()
		print("Database closed.")
		
	def __get_session(self):
		"""Returns Session object"""
		URI = 'sqlite:///' + self.filepath
		engine = create_engine(URI, echo=False)	
		
		Session = sessionmaker(bind=engine)
		return Session()
	
	def save(self):
		"""Saves changes made to the database."""
		self.session.commit()
		
		
	def add_goal(self, goal):
		"""Adds either a single row or multiple rows of data
			(goal object) to the database and saves.
			
		Params:
			goal	Goal object / a list of goal objects
		"""				
		if isinstance(goal, list):
			self.__add_multi_goal(goal)
		else:
			self.__add_one_goal(goal)
		self.save()
			
	def __add_one_goal(self, goal):
		"""Adds a single row of data
			(goal object) to the database if it is not a duplicate.
			
		Params:
			Goal object of the goal to be added
		"""		
		if self.contains_goal(goal.goal):
			print("Duplicate.")
		else:
			self.session.add(goal)
			
	def __add_multi_goal(self, goals):
		"""Adds a multiple rows of data
			(goal objects) to the database, filtering
			out duplicates.
			
		Params:
			List of goal objects to be added
		"""		
		dupl_array = [self.contains_goal(g.goal) for g in goals]
		do_add = [not i for i in dupl_array]
		
		unique_goals = [g for i, g in enumerate(goals) if do_add[i]]		
		self.session.add_all(unique_goals)
	
	def contains_goal(self, goal):
		"""Checks whether the goal is already within the database.
		
		Params:
			goal	String or Goal object.

		Returns:
			True if goal is already in the database,
			False otherwise.
		"""		
		if isinstance(goal, str):
			goal_str = goal
		else:
			goal_str = goal.goal
		return self.__contains_str(goal_str, "Goal")
	
	
	def add_task(self, task, parent, deadline=None):
		"""Adds task to the database and binds it to a parent
			(either a parent task or a goal).
			
		Params:
			task		String of the task to be added.
			parent		Task or Goal object
			deadline	Deadline for completing the task (datetime format)
			
		Returns:
			Task object
		"""
		task_obj = self.__make_task_obj(task, parent, deadline)
		self.session.add(task_obj)
		self.save()
		
		if isinstance(parent, Task):
			parent.child_id = task_obj.id
			self.save()
			
		return task_obj
		
	def __make_task_obj(self, task, parent, deadline):
		"""Generates task object for the given task string, parent and deadline.
			
		Params:
			task		String of the task to be added.
			parent		Task or Goal object
			deadline	Deadline for completing the task (datetime format)
			
		Returns:
			Task object
		"""
		if isinstance(parent, Goal):
			return Task(task=task, goal_id=parent.id, deadline=deadline)
		elif isinstance(parent, Task):
			return Task(task=task,
							goal_id=parent.goal_id,
							parent_id=parent.id,
							deadline=deadline)
		else:
			raise TypeError("Undefined parent type! Must be either Goal or Task.")
	
	def contains_task(self, task):
		"""Checks whether the task is already within the database.
		
		Params:
			task	String or Task object.

		Returns:
			True if task is already in the database,
			False otherwise.
		"""
		if isinstance(task, str):
			task_str = task
		else:
			task_str = task.task
		return self.__contains_str(task_str, "Task")
		
			
	def __contains_str(self, item, type):
		"""Checks whether the item string is already within the database
			as a goal or a task.
		
		Params:
			item	String of the goal or task to be queried.

		Returns:
			True if the item is already in the database,
			False otherwise.
		"""		
		if type == "Goal":
			contained = self.query_goal(item)
		elif type == "Task":
			contained = self.query_task(item)
			
		if contained:
			return True
		else:
			return False

		
	def query(self, entity):
		"""Returns query object."""
		return self.session.query(entity)
		
	def query_goal(self, goal_str):
		"""Queries the goal by string."""
		return self.query(Goal).filter(Goal.goal == goal_str).first()
		
	def query_task(self, task_str):
		"""Queries the task by string."""
		return self.query(Task).filter(Task.task == task_str).first()
		
	def query_goal_id(self, goal_id):
		"""Queries the goals by id."""
		return self.query(Goal).filter(Goal.id == goal_id).first()
		
	def query_task_id(self, task_id):
		"""Queries the tasks by id."""
		return self.query(Task).filter(Task.id == task_id).first()
	
	def query_cat(self, category):
		""""Queries the goals under the requested category."""
		return self.query(Goal).filter_by(category=category).all()
						
	def get_children(self, parent):
		"""Returns the children of the goal/tasks."""
		if isinstance(parent, Goal):
			return self.query(Task).filter_by(goal_id=parent.id).all()
		elif isinstance (parent, Task):
			return self.query(Task).filter_by(parent_id=parent.id).all()
		else:
			raise TypeError("Parent must be either Goal or Task object.")
	
