import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def daily_route():
	html = render_template("accordian.html")
	return html

if __name__ == "__main__":
	app.run(debug = True)