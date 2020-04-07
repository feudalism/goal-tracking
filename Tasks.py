from anytree import Node, RenderTree

class Tasks(object):
	"""
	Class of task objects corresponding to the goal,
	displayed as a tree.
	"""
	
	def __init__(self, goal):
		"""
		Initialises a task with the goal as the parent of the tree.
		"""
		self.root = Node(goal)
		
	def add(self, task, parent=None):
		if parent is None:
			parentNode = self.root
		else:
			parentNode = parent
		return Node(task, parent=parentNode)
		
	def print(self):
		for pre, fill, node in RenderTree(self.root):
			print("%s%s" % (pre, node.name))
		
	