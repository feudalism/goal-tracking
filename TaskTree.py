from anytree import Node, RenderTree

from db_creator import Goal

class TaskTree(object):
	"""
	Class of task objects corresponding to the goal,
	displayed as a tree.
	"""
	
	def __init__(self, tasks, do_print=True):
		"""
		Initialises a task with the goal as the parent of the tree.
		"""
		self.all_tasks = tasks
		self.main_tasks = None
		
		self.goal = self.get_goal()
		self.root = self.get_root()
		
		self.do_print = do_print
		
		self.set_up()
		self.print()
		
	def get_goal(self):
		main_tasks = [t for t in self.all_tasks if t.parent_id==None]
		if main_tasks == []:
			return None
		else:
			self.main_tasks = main_tasks
			return self.main_tasks[0].goal
			
	def get_root(self):
		root_str = "Goal: " + self.get_string(self.goal)		
		return Node(root_str)
		
	def get_string(self, obj):
		if isinstance(obj, Goal):
			str = obj.goal
		else:
			str = obj.task
		
		if obj.deadline:
			str = str + f"[{obj.deadline}]"
			
		return str
		
	def set_up(self):
		for m in self.main_tasks:
			self.iterate_over_children(m, self.root, self.all_tasks)
		
	def iterate_over_children(self, task, parent_node, all_tasks):
		node_str = self.get_string(task)
		task_node = Node(node_str, parent=parent_node)
		has_child = task.child_id
		
		if has_child is not None:
			children = self.query_by_parent(all_tasks, task)
			
			for c in children:
				self.iterate_over_children(c, task_node, all_tasks)
				
	def query_by_parent(self, all_tasks, parent):
		return [t for t in all_tasks if t.parent_id == parent.id]
		
	def print(self):
		if self.do_print:
			for pre, fill, node in RenderTree(self.root):
				print("%s%s" % (pre, node.name))
		
	