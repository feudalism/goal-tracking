from context import *

import unittest
import os, time
from shutil import copy, move
	
def addtests(suite, class_):
	tests = [class_(k) for k in class_.__dict__ if 'test' in k]
	suite.addTests(tests)

class TestDatabase(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		filename = 'test.db'
		
		self.filepath = os.path.join(REL_DIR, filename)
		self.data = (('goal1', 'cat1'), ('goal2', 'cat2'))
		self.newdata_one = (('goal5', 'cat1'))
	
	def setUp(self):
		self.db = db.init_db(self.filepath)
		self.cursor, _ = self.db
		self.assertTrue(self.check_exist)
		
		db.data_entry(self.data, self.db)
		
	def check_exist(self):
		return os.path.isfile(self.filepath)
		
	def check_goals_added(self, newdata):
		self.assertTrue(db.is_goals_added(self.db, newdata))
		
	def test_create_db(self):
		self.check_goals_added(self.data)
		
	def test_append_existing_goals(self):
		db.data_entry(self.data, self.db)
		self.check_goals_added(self.data)
			
	def test_append_new_data(self):
		newdata = (('goal3', 'cat1'), ('goal4', 'cat2'))
		db.data_entry(newdata, self.db)
		self.check_goals_added(newdata)
			
	def test_append_new_data_single(self):
		newdata = ('goal5', 'cat1')
		db.data_entry(newdata, self.db)
		self.check_goals_added(newdata)
		
	def tearDown(self):
		db.close(self.db)
		os.remove(self.filepath)
		self.assertFalse(self.check_exist())

class TestCategories(unittest.TestCase):	
	"""
	https://github.com/dvdme/forecastiopy/tree/master/tests
	"""
	@classmethod
	def setUpClass(self):
		filename = 'categories.txt'
		
		self.filepath = os.path.join(REL_DIR, filename)
		self.cats = ['cat1', 'cat2']
		self.newcats = ['cat1', 'cat4', 'cat5']
		
	def check_exist(self):
		return categories.is_file_exist(filepath=self.filepath)
		
	def create_file(self):
		categories.save_to_file(self.cats, self.filepath)
		self.assertTrue(self.check_exist())
		
	def remove_csv(self):
		os.remove(self.filepath)
		self.assertFalse(self.check_exist())
		
	def get_from_file(self):
		return categories.get_from_file(self.filepath)

	def test_create_cat_file(self):
		self.assertFalse(self.check_exist())		
		self.create_file()	
		
	def test_append_existing_cats(self):
		self.create_file()
		categories.save_to_file(self.cats, self.filepath)
		self.assertTrue(self.cats == self.get_from_file())
		
	def test_append_new_cats(self):
		self.create_file()
		categories.save_to_file(self.newcats, self.filepath)
		self.assertEqual(self.newcats, self.get_from_file())
		
	def tearDown(self):
		self.remove_csv()
		
class TestWorksheet(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.oldpath = os.path.join(REL_DIR, "all_goals.xlsx")
		
	def setUp(self):
		self.restore_path = self.oldpath + "temp"
		copy(self.oldpath, self.restore_path)
		
	def data_length(self, path):
		_, ws, _ = worksheet.extract_data(path)
		return ws.max_row

	def test_add_existing_goals(self):
		newpath = os.path.join(REL_DIR, "./existing_goals.xlsx")
		
		is_add = worksheet.add_new_goals(newpath, self.oldpath)		
		self.assertFalse(is_add)
		
	def test_add_new_goals(self):
		newpath = os.path.join(REL_DIR, "./new_goals.xlsx")
		
		old_len = self.data_length(self.oldpath)
		is_add = worksheet.add_new_goals(newpath, self.oldpath)	
		
		updated_len = self.data_length(self.oldpath)	
		self.assertGreater(updated_len, old_len)
		self.assertTrue(is_add)
		
		self.sel_tearDown()
		
		
	def sel_tearDown(self):
		view_chg_in_file = os.path.join(REL_DIR, "./temp.xlsx")
		copy(self.oldpath, view_chg_in_file)
		copy(self.restore_path, self.oldpath)
		os.remove(self.restore_path)
		
class TestGoalRemoval(unittest.TestCase):
	def setUp(self):
		self.oldpath = os.path.join(REL_DIR, "all_goals.xlsx")
		
		self.restore_path = self.oldpath + "temp"
		copy(self.oldpath, self.restore_path)
		
	def init_db(self):
		self.db_filepath = os.path.join(REL_DIR, "removal.db")
		self.db = db.init_db(self.db_filepath)
		self.cursor, self.conn = self.db
		
	def ws_to_db(self):
		data, self.ws, self.wb = worksheet.extract_data(self.oldpath)
		db.data_entry(data, self.db)
		
	def remove_line_from_ws(self):
		self.ws.delete_rows(self.ws.max_row)
		self.wb.save(self.oldpath)
		
	def test_remove_goal_from_db(self):
		self.init_db()
		self.ws_to_db()
		
		orig_data = db.fetch_all(self.cursor)
		orig_len = len(orig_data)
		
		self.remove_line_from_ws()
		worksheet.remove_goal_from_db(self.db, self.oldpath)
		
		truncated_data = db.fetch_all(self.cursor)
		mod_len = len(truncated_data)
		
		self.assertLess(mod_len, orig_len)
		
	def tearDown(self):
		move(self.restore_path, self.oldpath)

		
		
if __name__ == '__main__':
	# unittest.main()	
	
	suite = unittest.TestSuite()
	addtests(suite, TestDatabase)
	addtests(suite, TestCategories)
	addtests(suite, TestWorksheet)
	addtests(suite, TestGoalRemoval)
	
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)