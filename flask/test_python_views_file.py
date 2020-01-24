#! /usr/bin/python
import os
import requests
import json
import pandas as pd
from pet_functions import GetBearerToken
from pet_functions import GetTextResp

KEY = os.environ['PETFINDER_KEY']
SECRET = os.environ['PETFINDER_SECRET']

shelter_id = 'NV16'
my_header = GetBearerToken(KEY = KEY, SECRET = SECRET)

df_to_display = GetTextResp(organization = shelter_id, header = my_header)

print(df_to_display.head())

