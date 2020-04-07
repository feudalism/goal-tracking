import sqlite3

from paths import DB_FILEPATH

	
def init_db(filepath=DB_FILEPATH):
	cursor, connection = connect(filepath)
	create_table(cursor)
	
	return cursor, connection
	
def connect(filepath=DB_FILEPATH):
	connection = sqlite3.connect(filepath)
	cursor = connection.cursor()
	return cursor, connection
	
def close(db):
	cursor, connection = db
	cursor.close()
	connection.close()

def create_table(cursor):
	cursor.execute('''CREATE TABLE IF NOT EXISTS maingoals
		(id INTEGER PRIMARY KEY, goal TEXT, category TEXT)''')
	
def is_goals_added(db, newdata):
	newdata = remove_existing_goals(db, newdata)
	
	if newdata:
		return False
	else:
		return True
		

def get_goals_from_cat(cat, database):
	cursor, conn = database
	t = (cat,)
	
	cursor.execute("SELECT goal FROM maingoals where category=?", t)
	return {goal[0] for goal in cursor.fetchall()}
		
def single_data_entry(data, db):
	cursor, connection = db
	cursor.execute('INSERT INTO maingoals (goal, category) VALUES(?, ?)', data )
	connection.commit()
	
def multi_data_entry(data, db):
	for item in data:
		single_data_entry(item, db)
	
def fetch_all(cursor):
	cursor.execute("SELECT goal, category FROM maingoals")
	return cursor.fetchall()
	
def is_goal_in_db(data, db):
	cursor, conn = db
	goal, _ = data
	t = (goal,)
	
	cursor.execute("SELECT goal FROM maingoals where goal=?", t)
	result = cursor.fetchone()
	
	if result == None:
		return False
	else:
		return True
		
def remove_existing_goals(db, newdata):
	data = []
	single = is_single_data(newdata)
	
	if single:
		existing = is_goal_in_db(newdata, db)
		if not existing:
			data = newdata
	else:
		for item in newdata:
			existing = is_goal_in_db(item, db)
			
			if not existing:
				data.append(item)
	
	return data
	
def is_single_data(data):
	if not isinstance(list(data)[0], tuple):
		return True
	else:
		return False
		
def data_entry(newdata, db):
	data = remove_existing_goals(db, newdata)
	
	if data:
		print("New goal(s) to be added...")
		
		single = is_single_data(data)
		if single:
			single_data_entry(data, db)
		else:
			multi_data_entry(data, db)