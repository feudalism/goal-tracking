import sqlite3

class GoalsDb(object):
	"""
	Database of goals.
	"""
	
	def __init__(self, name, filepath):
		"""
		Creates an database file with an empty table.
		"""
		self.name = name
		self.filepath = filepath
		self.connection = sqlite3.connect(self.filepath)
		self.cursor = self.connection.cursor()
		
		self.create_table()
		self.save()
		print("Initialised database.")
		
	def __del__(self):
		"""
		Closes the cursor and connection before shutdown.
		"""
		self.cursor.close()
		self.connection.close()
		print("Database closed.")
		
	def save(self):
		"""
		Saves changes made to the database.
		"""
		self.connection.commit()
		
	def create_table(self):
		"""
		Creates an empty table.
		"""
		query = f"""CREATE TABLE IF NOT EXISTS {self.name}
			(goal TEXT PRIMARY KEY,
			category TEXT,
			tasks BLOB)"""
		self.cursor.execute(query)
		
	def add_goal(self, data):
		"""
		Adds either a single row or multiple rows of data
		(goal, category) to the database.
		"""
		query = f"INSERT OR IGNORE INTO {self.name} (goal, category) VALUES(?, ?)"
		
		if isinstance(data[0], tuple):
			self.cursor.executemany(query, data)
		else:
			self.cursor.execute(query, data)
		self.save()
		
	def is_contains_goal(self, goal):
		"""
		Checks whether the goal is already within the database.
		"""
		query = f"SELECT goal FROM {self.name} where goal=?"
		t = (goal,)
		self.cursor.execute(query, t)
		
		result = self.cursor.fetchall()
		assert(len(result) == 1)
		
		if result:
			print(f"Goal \'{goal}\' is already inside the database.")
			return True
		else:
			return False
		
	def query_cat(self, category):
		""""
		Queries the goals under the requested category.
		"""
		query = f"SELECT goal FROM {self.name} where category=?"
		t = (category,)
		
		self.cursor.execute(query, t)
		return {data[0] for data in self.cursor.fetchall()}
		
		
	# def query_all(self):
		# """
		# Gets all entries of the database.
		# """
		# query = f"SELECT * FROM {self.db.name}"
		# self.db.cursor.execute(query)
		# return self.db.cursor.fetchall()
		
	
