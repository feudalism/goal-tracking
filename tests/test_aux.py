import os
from shutil import copy, move

def addtests(suite, class_):
	tests = [class_(k) for k in class_.__dict__ if 'test' in k]
	suite.addTests(tests)
	
def file_exists(filepath):
	return os.path.isfile(filepath)
	
def make_backup(src_filepath):
	dst_filepath = src_filepath + "temp"
	copy(src_filepath, dst_filepath)
	
def restore_backup(src_filepath):
	backup_filepath = src_filepath + "temp"
	move(backup_filepath, src_filepath)
	
def remove_file(filepath):
	try:
		os.remove(filepath)
	except FileNotFoundError:
		pass
		