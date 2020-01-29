import os
import requests 
import json
import pandas as pd 
import sklearn
import pickle
import numpy as np

KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

def get_bearer_token(KEY,SECRET):
	data = {
	'grant_type': 'client_credentials',
	'client_id': KEY,
	'client_secret': SECRET
	  }
	response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)
	if response.reason != 'OK':
	    print('failed to get token. check credentials')
	    print('response code:', response.status_code)
	    print('response reason:', response.reason)
	else:
	    print('new token received')
	    TOKEN = json.loads(response.text)['access_token']
	    new_header = {
	            'Authorization': 'Bearer {}'.format(TOKEN),}
	return new_header


def get_text_resp(organization, header):
	org = organization
	type = 'dog'
	page = 1
	limit = 100
	status = 'adoptable'
	respdf = pd.DataFrame()
	req_url = f'https://api.petfinder.com/v2/animals?type={type}&limit={limit}&page={page}&status={status}&organization={org}'
	response = requests.get(req_url, headers = header)
	my_dict =json.loads(response.text)
	animals = my_dict.get('animals')
	df = pd.io.json.json_normalize(animals)
	respdf = respdf.append(df)
	return respdf

def clean_dirty_resp(df):
	my_df = df 
	my_df = my_df[['age','gender','size','coat','attributes.special_needs','name','id']]
	#city should be here!
	#other cleaning?
	#uf the columns expected by the model don't exist, create them and fill them with zeros
	return my_df



def get_petmod_predict(df):
	vars_of_interest =['age','size', 'coat','attributes.special_needs']
	cols_to_transform = ['age','size', 'coat','attributes.special_needs']
	my_df = df
	X = my_df[vars_of_interest]
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
	my_df['predicted_percent'] = round(my_df['predicted_probability']*100)

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
	my_df['predicted_percent_ElPaso'] = round((my_df['predicted_prob_ElPaso']*100),0)

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
	pred_y3s = loaded_model.predict_proba(X3)
	my_df['predicted_prob_Minne'] = pred_y3s[:,1] 
	my_df['predicted_percent_Minne'] = round(my_df['predicted_prob_Minne']*100)


	return my_df





