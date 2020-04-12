from db_setup import app, db		## -- uses DB_FILEPATH AND A NEW INSTANCE OF APP

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# from paths import DB_FILEPATH
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILEPATH

# def init_db(filepath):
# # CREATE ENGINE FROM FILEPATH
# engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
# # CREATE SESSION BOUND TO THE ENGINE
# session = scoped_session(sessionmaker(autocommit=False,
										 # autoflush=False,
										 # bind=engine))
# # # CREATE DECLARATIVE BASE AND BIND IT TO SESSION
# Base = declarative_base()
# Base.query = session.query_property()

# # IMPORT MODELS -- WHICH USES AN INSTANCE OF DB
# # BASE CREATE_ALLB
import models	## -- DB_SETUP (YET NEW INSTANCE OF APP) -- ## APPARENTLY NOT
# Base.metadata.create_all(bind=engine)
db.create_all()

# # DEFINE APP ROUTE
from website import routes ## db_setup

# # APP RUN
app.run()






# from db_setup import dump_db as db

# from db_setup import init_db



# dump_db.init_app(app)

# with app.app_context():
	# import models

# init_db(filepath)


# app.run(debug=True)



# ######
# # https://www.blog.pythonlibrary.org/2017/12/12/flask-101-adding-a-database/

