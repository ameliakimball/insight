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
from pet_functions import GetPetmodPredict


KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

shelter_id = 'il132'

my_header = GetBearerToken(KEY = KEY, SECRET = SECRET)
dirty_df = GetTextResp(organization = shelter_id, header = my_header)
clean_df = CleanDirtyResp(df= dirty_df)

X = clean_df[['age','gender','size','City']]
cols_to_transform = ['age', 'gender', 'size','City']
X = pd.get_dummies(X, columns = cols_to_transform )
X['age_Baby'] = 0
X['age_Senior'] = 0
X['size_Small'] = 0
X['size_Extra Large'] = 0
X['City_StLouis'] = 0 
X['City_Indy'] = 0

print(X.head())

filename = 'draft_pet_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
pred_ys = loaded_model.predict(X)
clean_df['pred_ys'] = pred_ys
print(clean_df.head())




