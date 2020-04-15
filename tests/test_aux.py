# Helper functions for the test suites
import os
from shutil import copy, move

REL_DIR, _ = os.path.split(__file__)

def addtests(suite, class_):
	tests = [class_(k) for k in class_.__dict__ if 'test' in k]
	suite.addTests(tests)
	
def file_exists(filepath):
	return os.path.isfile(filepath)
		
def abs_path(filepath):
	return os.path.join(REL_DIR, filepath)
	
def duplicate(src_filepath, dst_filepath):
	copy(src_filepath, dst_filepath)
	
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