import os
import numpy as np
import json
import pickle
from flask import render_template
from flask import request 
from flaskexample import app
import pandas as pd
import requests
from pet_functions import get_bearer_token
from pet_functions import get_text_resp
from pet_functions import clean_dirty_resp
from pet_functions import get_petmod_predict


KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

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
  shelter_id = request.args.get('shelter_id')
  my_header = get_bearer_token(KEY = KEY, SECRET = SECRET)
  dirty_df = get_text_resp(organization = shelter_id, header = my_header)
  clean_df = clean_dirty_resp(df= dirty_df)
  predict_df = get_petmod_predict(df = clean_df)
  top_dogs = predict_df.nsmallest(10,'predicted_percent')
  df_to_display = top_dogs.sort_values(by=['predicted_percent'])
  #what if you enter a shelter with fewer than 10 dogs?
  return render_template("output.html", mydf = df_to_display, my_range = range(0,20))
