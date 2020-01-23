#! usr/bin/python

import os 
import requests
import json
import pandas as pd

KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

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
            'Authorization': 'Bearer {}'.format(TOKEN),
        }


organization = 'NV16'
type = 'dog'
page = 1
limit = 100
status = 'adoptable'

respdf = pd.DataFrame()

req_url = f'https://api.petfinder.com/v2/animals?type={type}&limit={limit}&page={page}&status={status}&organization={organization}'
response = requests.get(req_url, headers= new_header)
print(response)
my_dict =json.loads(response.text)
animals = my_dict.get('animals')
df = pd.io.json.json_normalize(animals)
respdf = respdf.append(df)


#clean and preprocess the input data 


#load model and make predictions 

loaded_model = pickle.load(open('draft_pet_model.sav', 'rb'))







