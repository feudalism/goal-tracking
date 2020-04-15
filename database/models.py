from .setup import db

class Goal(db.Model):
	__tablename__ = 'goals'
	
	id = db.Column(db.Integer, primary_key=True)
	goal = db.Column(db.String, unique=True, nullable=False)
	category = db.Column(db.String, nullable=False)
	deadline = db.Column(db.DateTime, nullable=True)
	
	# One-to-many G > T*
	tasks = db.relationship("Task", back_populates="goal")
	
	def __repr__(self):
		return f"<GOAL {self.id}: \'{self.goal}\' [{self.category}]>"
		
class Task(db.Model):
	__tablename__ = 'tasks'
	
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String, nullable=False)
	deadline = db.Column(db.DateTime, nullable=True)
	
	# One-to-many G > T*
	goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
	goal = db.relationship("Goal", back_populates="tasks")
	
	# One-to-many T > ST*
	parent_id = db.Column(db.Integer)
	child_id = db.Column(db.Integer)
	
	def __repr__(self):
		return f"<TASK \'{self.task}\'>"
		