
from flask import render_template, url_for

@app.route("/")
def hello():
	# return "Hello, world."
	return render_template('dashboard.html')