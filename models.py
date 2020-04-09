from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import LargeBinary


Base = declarative_base()

class Goal(Base):
	__tablename__ = 'goals'
	
	goal = Column(String, primary_key=True)
	category = Column(String)
	tasks = LargeBinary(String)
	
	def __repr__(self):
		return f"<Goal \'{self.goal}\' [{self.category}]>"
		