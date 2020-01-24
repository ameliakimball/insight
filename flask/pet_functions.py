import os
import requests 
import json
import pandas as pd 
import sklearn
import pickle
import numpy as np

KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

def GetBearerToken(KEY,SECRET):
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


def GetTextResp(organization, header):
	org = organization
	type = 'dog'
	page = 1
	limit = 25
	status = 'adoptable'

	respdf = pd.DataFrame()
	req_url = f'https://api.petfinder.com/v2/animals?type={type}&limit={limit}&page={page}&status={status}&organization={org}'
	response = requests.get(req_url, headers = header)
	my_dict =json.loads(response.text)
	animals = my_dict.get('animals')
	df = pd.io.json.json_normalize(animals)
	respdf = respdf.append(df)
	return respdf

def CleanDirtyResp(df):
	my_df = df 
	my_df = my_df[['age','gender','size','name','id']]
	my_df['City'] = 'Chicago' #FIXME
	return my_df

def GetPetmodPredict(df):
	my_df = df 
	X = my_df[['age','gender','size','City']]
	cols_to_transform = ['age', 'gender', 'size','City']
	X = pd.get_dummies(X, columns = cols_to_transform )
	X['age_Baby'] = 0
	X['age_Senior'] = 0
	X['size_Small'] = 0
	X['size_Extra Large'] = 0
	X['City_StLouis'] = 0 
	X['City_Indy'] = 0
	filename = 'draft_pet_model.sav'
	loaded_model = pickle.load(open(filename, 'rb'))
	pred_ys = loaded_model.predict(X)
	my_df['pred_ys'] = np.log(pred_ys)
	return my_df






