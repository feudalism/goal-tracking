from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
db.init_app(app)