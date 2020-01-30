#! /usr/bin/python
import os
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
from pet_functions import one_hot_fill
from pet_functions import get_petmod_predict


KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

shelter_id = 'il537'

my_header = get_bearer_token(KEY = KEY, SECRET = SECRET)
dirty_df = get_text_resp(organization = shelter_id, header = my_header)
clean_df = clean_dirty_resp(df= dirty_df,
							vars_of_interest = ['age','size','coat',
												'attributes.special_needs',
												'name','id'])

coded_df = one_hot_fill(df = clean_df)
                       #  cols_to_transform = ['age','size','coat','attributes.special_needs'])


X = coded_df.drop(['name', 'id'], axis=1)

filename = 'draft_logit_reg.sav'
loaded_model = pickle.load(open(filename, 'rb'))
pred_ys = loaded_model.predict_proba(X)
coded_df['predicted_probability'] = pred_ys[:,1] 
coded_df['predicted_percent'] = round(coded_df['predicted_probability']*100)

print(coded_df.head())

	# ElPaso = df
	# ElPaso['City_Chicago'] = 0
	# ElPaso['City_StLouis'] = 0
	# ElPaso['City_Indy'] = 0
	# ElPaso['City_Houston'] = 0
	# ElPaso['City_ElPaso'] = 1
	# ElPaso['City_Minne'] = 0
	# ElPaso['City_Minne'] = 0
	# pred_y2s = loaded_model.predict_proba(ElPaso)
	# my_df['predicted_prob_ElPaso'] = pred_y2s[:,1] 
	# my_df['predicted_percent_ElPaso'] = round((my_df['predicted_prob_ElPaso']*100),0)








