from db_setup import app
from models import Goal

from flask import render_template, url_for
from flask_table import Table, Col, LinkCol

class GoalsTable(Table):
	table_id = "goals_table"
	allow_sort = True

	def sort_url(self, col_key, reverse=True):
		if reverse:
			direction =  'desc'
		else:
			direction = 'asc'
		return url_for('index', sort=col_key, direction=direction)
	
	id = Col('Id', show=False)
	goal = Col('Goal')
	category = Col('Category')
	deadline = Col('Deadline', show=False)
	edit = LinkCol('View', 'edit', url_kwargs=dict(id='id'))
	
def generate_table():
	goals = Goal.query.order_by( Goal.deadline.asc() )
	
	query_dict = {}
	query_list = []
	for g in goals:
		query_dict['id'] = g.id
		query_dict['goal'] = g.goal
		query_dict['category'] = g.category
		
		query_list.append(query_dict)
		query_dict = {}
		
	return GoalsTable(query_list)
		
@app.route("/")
def index():
	goals_table = generate_table()
	return render_template('dashboard.html', table=goals_table)
	
@app.route("/item/<int:id>", methods=['GET', 'POST'])
def edit(id=id):
	goal_obj = Goal.query.filter( Goal.id == id ).first()
	goal = goal_obj.goal
	return render_template('goal.html', goal=goal)