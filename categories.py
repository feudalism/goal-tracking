import os

FILEPATH = 'categories.txt'

def get(data):
	cats = {cat for (_, cat) in list(data)}	
	return sorted(cats)
		
def get_from_file(filepath=FILEPATH):
	with open(filepath, 'r') as file:
		cats = [row.strip() for row in file]	
		return cats

def is_file_exist(filepath=FILEPATH):
	if os.path.isfile(filepath):
		return True
	else:
		return False

def is_unchanged(from_data, filepath=FILEPATH):
	from_file = get_from_file(filepath)
	return from_data == from_file
	
def write_cats(cats, filepath=FILEPATH):
	with open(filepath, 'w+') as file:
		for cat in cats:
			file.write(f"{cat}\n")
	
def save_to_file(cats, filepath=FILEPATH):
	file_exists = is_file_exist(filepath)
	
	if file_exists and is_unchanged(cats, filepath):
		pass
	else:
		print("Updating categories...")
		write_cats(cats, filepath)
		