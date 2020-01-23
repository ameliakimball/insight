
from flask import render_template
from flask import request 
from flaskexample import app
import pandas as pd


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Dog lover, go to the input page to test the app' },
       )

@app.route('/input')
def cesareans_input():
    return render_template("input.html")

@app.route('/output')
def cesareans_output():
  #pull 'shelter_id' from input field and store it
  #patient = request.args.get('shelter_id')
  mylist_of_dicts = [{'amelia':'The best', 'dogs':'alsogreat','cats':'less so'},{'amelia':'notsogreat', 'dogs':'alsogreat','cats':'less so'}]
  return render_template("output.html", mylist_of_dicts = mylist_of_dicts)
