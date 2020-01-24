import os
import numpy as np
import json
import pickle
from flask import render_template
from flask import request 
from flaskexample import app
import pandas as pd
import requests
from pet_functions import GetBearerToken
from pet_functions import GetTextResp
from pet_functions import CleanDirtyResp
from pet_functions import GetPetmodPredict

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
  my_header = GetBearerToken(KEY = KEY, SECRET = SECRET)
  dirty_df = GetTextResp(organization = shelter_id, header = my_header)
  clean_df = CleanDirtyResp(df= dirty_df)
  df_to_display = GetPetmodPredict(df = clean_df)
  return render_template("output.html", mydf = df_to_display, my_range = range(0,20))
