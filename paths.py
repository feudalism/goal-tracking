import os

PATH = 'C:\\Users\\user3\\Downloads\\'

NG_FILENAME = 'new_goals.xlsx'
NG_FILEPATH = os.path.join(PATH, NG_FILENAME)

AG_FILENAME = 'all_goals.xlsx'
AG_FILEPATH = os.path.join(PATH, AG_FILENAME)

DB_FILE = 'all_goals.db'
DB_FILEPATH = os.path.join(PATH, DB_FILE)

TEST_FILE = 'test_website.db'
TEST_DIR = 'C:\\Users\\user3\\Dropbox\\test\\goals\\tests'
TEST_FILEPATH = os.path.join(TEST_DIR, TEST_FILE)