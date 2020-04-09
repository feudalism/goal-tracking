import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import categories
import db
import worksheet

from GoalsDb import GoalsDb
from Tasks import Tasks
from models import *

from test_aux import *

REL_DIR, _ = os.path.split(__file__)