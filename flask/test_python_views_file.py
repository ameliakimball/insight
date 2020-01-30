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

shelter_id = 'nv36'
my_header = get_bearer_token(KEY = KEY, SECRET = SECRET)
dirty_df = get_text_resp(organization = shelter_id, header = my_header)
clean_df = clean_dirty_resp(df= dirty_df, vars_of_interest =['age','size', 'coat','attributes.special_needs','name','id'])

coded_df = one_hot_fill(df = clean_df,
	cols_in_mod = ['age_Adult', 'age_Baby', 'age_Senior', 'age_Young', 'City_Chicago', 'City_Denver', 'City_ElPaso', 'City_Houston', 'City_Indy', 'City_Minne', 'City_StLouis', 'size_Extra Large','size_Large', 'size_Medium', 'size_Small','coat_Curly', 'coat_Hairless', 'coat_Long','coat_Medium', 'coat_Short', 'coat_Wire','attributes.special_needs_False','attributes.special_needs_True'],
	cols_to_transform = ['age','size', 'coat','attributes.special_needs'])

predict_df = get_petmod_predict(coded_df = coded_df)

print(predict_df.head(10))
print(predict_df.name.to_string(index=False))
#X = coded_df.drop(['name','id'],1)
#filename = 'draft_logit_reg.sav'
#loaded_model = pickle.load(open(filename, 'rb'))
#pred_ys = loaded_model.predict_proba(X)
#coded_df['predicted_probability'] = pred_ys[:,1] 
#coded_df['predicted_percent'] = round(coded_df['predicted_probability']*100)

#new_df = coded_df.sort_values(by='predicted_percent', axis =0, inplace=False)



# X = coded_df.drop(['name','id'],1)
# filename = 'draft_logit_reg.sav'
# loaded_model = pickle.load(open(filename, 'rb'))
# pred_ys = loaded_model.predict_proba(X)
# my_df['predicted_probability'] = pred_ys[:,1] 
# my_df['predicted_percent'] = round(my_df['predicted_probability']*100)


# Denver = coded_df.drop(['name','id'],1)
# Denver['City_Chicago'] = 0
# Denver['City_StLouis'] = 0
# Denver['City_Indy'] = 0
# Denver['City_Houston'] = 0
# Denver['City_ElPaso'] = 0
# Denver['City_Denver'] = 1
# Denver['City_Minne'] = 0
# pred_y2s = loaded_model.predict_proba(Denver)

# my_df['predicted_prob_Denver'] = pred_y2s[:,1] 
# my_df['predicted_percent_Denver'] = round((my_df['predicted_prob_Denver']*100),0)

# Houston = coded_df.drop(['name','id'],1)
# Houston['City_Chicago'] = 0
# Houston['City_StLouis'] = 0
# Houston['City_Indy'] = 0
# Houston['City_Houston'] = 1
# Houston['City_ElPaso'] = 0
# Houston['City_Denver'] = 0
# Houston['City_Minne'] = 0
# pred_y3s = loaded_model.predict_proba(Houston)

# my_df['predicted_prob_Houston'] = pred_y3s[:,1] 
# my_df['predicted_percent_Houston'] = round((my_df['predicted_prob_Houston']*100),0)

# top_dogs = my_df.nsmallest(10,'predicted_probability')
# df_to_display = top_dogs.sort_values(by=['predicted_probability'])


#print(top_dogs.head(10))







