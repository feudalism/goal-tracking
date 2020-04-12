import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import categories
import db
import website
import worksheet

from GoalsDb import GoalsDb
from TaskTree import TaskTree
from models import *

from test_aux import *

REL_DIR, _ = os.path.split(__file__)