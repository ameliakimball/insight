#! /usr/bin/python
import os
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


KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

shelter_id = 'il537'

my_header = GetBearerToken(KEY = KEY, SECRET = SECRET)
dirty_df = GetTextResp(organization = shelter_id, header = my_header)
clean_df = CleanDirtyResp(df= dirty_df)

my_df = clean_df

X = my_df[['age','size', 'coat','attributes.special_needs']]
cols_to_transform = ['age','size', 'coat','attributes.special_needs']
X = pd.get_dummies(X, columns = cols_to_transform )
X.insert(0, 'size_Extra Large', 0)
X.insert(0, 'coat_Hairless', 0)
X.insert(0, 'City_StLouis', 0)
X.insert(0, 'City_Indy', 0)
X.insert(0, 'City_Houston', 0)
X.insert(0, 'City_ElPaso', 0)
X.insert(0, 'City_Minne', 0)
X.insert(0, 'City_Denver', 0)
X.insert(0, 'City_Chicago', 1)#this should not be hard coded!  


filename = 'draft_logit_reg.sav'
loaded_model = pickle.load(open(filename, 'rb'))
pred_ys = loaded_model.predict_proba(X)
my_df['predicted_probability'] = pred_ys[:,1] 
my_df['predicted_percent'] = my_df['predicted_probability']*100
my_df['predicted_percent'] = round(my_df['predicted_percent'],2)

X2 = my_df[['age','size', 'coat','attributes.special_needs']]
cols_to_transform = ['age','size', 'coat','attributes.special_needs']
X2 = pd.get_dummies(X2, columns = cols_to_transform )
X2.insert(0, 'size_Extra Large', 0)
X2.insert(0, 'coat_Hairless', 0)
X2.insert(0, 'City_StLouis', 0)
X2.insert(0, 'City_Indy', 0)
X2.insert(0, 'City_Houston', 0)
X2.insert(0, 'City_ElPaso', 1)
X2.insert(0, 'City_Minne', 0)
X2.insert(0, 'City_Denver', 0)
X2.insert(0, 'City_Chicago', 0)
pred_y2s = loaded_model.predict_proba(X2)
my_df['predicted_prob_ElPaso'] = pred_y2s[:,1] 
my_df['predicted_percent_ElPaso'] = round(my_df['predicted_prob_ElPaso']*100,2)


X3 = my_df[['age','size', 'coat','attributes.special_needs']]
cols_to_transform = ['age','size', 'coat','attributes.special_needs']
X3 = pd.get_dummies(X3, columns = cols_to_transform )
X3.insert(0, 'size_Extra Large', 0)
X3.insert(0, 'coat_Hairless', 0)
X3.insert(0, 'City_StLouis', 0)
X3.insert(0, 'City_Indy', 0)
X3.insert(0, 'City_Houston', 0)
X3.insert(0, 'City_ElPaso', 0)
X3.insert(0, 'City_Minne', 1)
X3.insert(0, 'City_Denver', 0)
X3.insert(0, 'City_Chicago', 0)
pred_y2s = loaded_model.predict_proba(X2)
my_df['predicted_prob_Minne'] = pred_y2s[:,1] 
my_df['predicted_percent_Minne'] = round(my_df['predicted_prob_Minne']*100,2)

#top_dogs = my_df.nsmallest(10,'predicted_percent')

print(my_df.head())



