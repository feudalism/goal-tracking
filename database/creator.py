from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Goal(Base):
	__tablename__ = 'goals'
	
	id = Column(Integer, primary_key=True)
	goal = Column(String, unique=True, nullable=False)
	category = Column(String, nullable=False)
	deadline = Column(DateTime, nullable=True)
	
	# One-to-many G > T*
	tasks = relationship("Task", back_populates="goal")
	
	def __repr__(self):
		return f"<GOAL {self.id}: \'{self.goal}\' [{self.category}]>"
		
class Task(Base):
	__tablename__ = 'tasks'
	
	id = Column(Integer, primary_key=True)
	task = Column(String, nullable=False)
	deadline = Column(DateTime, nullable=True)
	
	# One-to-many G > T*
	goal_id = Column(Integer, ForeignKey('goals.id'))
	goal = relationship("Goal", back_populates="tasks")
	
	# One-to-many T > ST*
	parent_id = Column(Integer)
	child_id = Column(Integer)
	
	def __repr__(self):
		return f"<TASK \'{self.task}\'>"
		
def create_tables(filepath):
	"""Creates a database with tables at the filepath,
		if none pre-existing."""
	engine = create_engine('sqlite:///' + filepath)
	Base.metadata.create_all(engine)