from models import Goal

from flask import current_app as app
from flask import render_template, url_for
from flask_table import Table, Col, LinkCol

class GoalsTable(Table):
	table_id = "goals_table"
	allow_sort = True
	
	def __init__(self, query_list, sorted_col, sorted_col_dir):
		super().__init__(query_list)
		self.sorted_col = sorted_col
		self.sorted_col_dir = sorted_col_dir

	def sort_url(self, col_key):
		if col_key == self.sorted_col:
			if self.sorted_col_dir == 'asc':
				rev_dir = 'desc'
			else:
				rev_dir = 'asc'
			return url_for('home_sort', col=col_key, dir=rev_dir)
			
		elif col_key is 'edit':
			return ""
			
		else:
			return url_for('home_sort', col=col_key, dir='asc')
	
	id = Col('Id')
	goal = Col('Goal')
	category = Col('Category')
	deadline = Col('Deadline', show=False)
	view = LinkCol('View', 'view', url_kwargs=dict(id='id'),
			th_html_attrs={'font-weight': 'bold'})
	
def generate_table(col='id', dir='asc'):
	order_eval = eval(f"Goal.{col}.{dir}()")
	goals = Goal.query.order_by( order_eval )
		
	return GoalsTable(goals,
				sorted_col = col,
				sorted_col_dir = dir)
	

@app.route("/")
def home():
	goals_table = generate_table()
	return render_template('home.html', table=goals_table)
	
@app.route("/?sort=<string:col>&dir=<string:dir>")
def home_sort(col, dir):
	goals_table = generate_table(col, dir)
	return render_template('home.html', table=goals_table)
	
@app.route("/item/<int:id>", methods=['GET', 'POST'])
def view(id=id):
	goal_obj = Goal.query.filter( Goal.id == id ).first()
	goal = goal_obj.goal
	return render_template('goal.html', goal=goal)