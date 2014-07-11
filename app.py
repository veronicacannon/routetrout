import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def daily_route():
	html = render_template("accordian.html")
	return html

@app.route('/json')
def json_example():
	html = render_template("json.html")
	return html

@app.route('/drop')
def select_pref():
    html = render_template("droppable.html")
    return html

@app.route('/define')
def define_health_alerts():
    html = render_template("define_health_alerts.html")
    return html

@app.route('/health')
def health_alerts():
    html = render_template("health_alerts.html")
    return html

if __name__ == "__main__":
	app.run(debug = True)