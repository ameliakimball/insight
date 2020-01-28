
#input will be the df created from the API


def calc_probabilities(df): #, 
                       #work_state): #, citizen_country): #, business_size):
    import numpy as np
    import pandas as pd
    import math
    import datetime as dt
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    from urllib.parse import urlparse
    import os
    import psycopg2


    database_url = os.environ.get('DATABASE_URL', None)
    result = urlparse(database_url)
    username = result.username
    password = result.password
    host = result.hostname
    port = '5432'
    db_name = result.path[1:]

    con = None
    con = psycopg2.connect(database = db_name, user = username, host=host, password=password)
    

    #load the pickled model 

    #get predictions for whole list of dogs 


    #make new predictions for a change in location 


    #return dataframe with prediction in current location, and three donor cities 


    