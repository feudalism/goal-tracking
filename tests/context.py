import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_aux import *

from database import *
from config import TestingConfig
from website.app import create_app