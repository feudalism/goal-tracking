from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DictExporter
from collections import OrderedDict
from pprint import pprint

from .creator import Goal

class TaskTree(object):
	"""Task objects corresponding to the goal,
		displayed as a tree."""
	
	def __init__(self, tasks, goal, do_print=False):
		"""Initialises a task with the goal as the parent of the tree."""
		self.goal = goal
		self.all_tasks = tasks
		self.root = self.__gen_root()
		
		self.do_print = do_print
		
		self.__set_up()
		if do_print:
			self.print()
			
	def __gen_root(self):
		"""Generate root node (goal)."""
		root_str = "GOAL: " + self.goal.goal
		return Node(root_str, item=self.goal)
		
	def __set_up(self):
		"""Iterates over all tasks and creates nodes for each of them."""
		main_tasks = [t for t in self.all_tasks if t.parent_id == None]
		for m in main_tasks:
			self.iterate_over_children(m, self.root)
		
	def iterate_over_children(self, task, parent_node):
		"""Recursively iterates over the task children, starting
			from a given parent node, and generates a node for
			each child.
			
		Params:
			task		Current task for which a node is to be generated.
			parent_node	Parent node of the current task."""
		node_str = self.__gen_string(task)
		task_node = Node(node_str, parent=parent_node, item=task)
		has_child = task.child_id
		
		if has_child is not None:
			children = [t for t in self.all_tasks if t.parent_id == task.id]
			for c in children:
				self.iterate_over_children(c, task_node)
		
	def __gen_string(self, task):
		"""Generates the string for the task, tacking on a deadline if available."""
		if task.deadline:
			return task.task + f"[{task.deadline}]"
		else:
			return task.task
		
	def print(self):
		"""Prints the task tree to console."""
		for pre, fill, node in RenderTree(self.root):
			print(f"{pre}{node.name}")
		
	def to_dict(self):
		"""Converts the task tree to an ordered dict."""
		exporter = DictExporter(dictcls=OrderedDict, attriter=sorted)
		return exporter.export(self.root)
		
		
		
	