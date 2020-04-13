import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_creator import *
from website.app import create_app
from config import TestingConfig

from GoalsDb import GoalsDb
from TaskTree import TaskTree

from test_aux import *

REL_DIR, _ = os.path.split(__file__)