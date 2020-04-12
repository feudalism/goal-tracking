from paths import DB_FILEPATH

from website import app
from flask_sqlalchemy import SQLAlchemy

app = app.init(DB_FILEPATH)
db = SQLAlchemy(app)


# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# def init_db(filepath):
	# engine = create_engine(filepath, convert_unicode=True)
	# db_session = scoped_session(sessionmaker(autocommit=False,
											 # autoflush=False,
											 # bind=engine))
	# Base = declarative_base()
	# Base.query = db_session.query_property()

	# import models
	# Base.metadata.create_all(bind=engine)
	# db.create_all()