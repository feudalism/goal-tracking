from database import TaskTree
from database.models import Goal, Task

from flask import current_app as app
from flask import render_template, url_for
from flask_table import Table, Col, LinkCol
from anytree import PreOrderIter

from .GoalsTable import *

@app.route("/")
def home():
	goals_table = generate_table()
	return render_template('home.html', table=goals_table)
	
@app.route("/?sort=<string:col>&dir=<string:dir>")
def home_sort(col, dir):
	if col != 'view':
		goals_table = generate_table(col, dir)
	else:
		goals_table = generate_table()
	return render_template('home.html', table=goals_table)
	
@app.route("/goal/<int:id>", methods=['GET', 'POST'])
def view(id=id):
	goals_table = generate_table()
	goal = Goal.query.filter( Goal.id == id ).first()
	tasks = Task.query.filter( Task.goal_id == goal.id )
	tasks_dict = TaskTree(tasks, goal, do_print=False).to_dict()
	
	return render_template('goal.html', table=goals_table, goal=goal.goal, tasks=tasks_dict)