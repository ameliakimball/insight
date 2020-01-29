
#input will be the df created from the API

#run a linter : pylint 

def calc_probabilities(df, mod_features, disc_features): #, 
                       #work_state): #, citizen_country): #, business_size):
   # if  
    #    raise ValueError('df must be a dataframe')
    #mod features must be a list 
    #disc_features must a list and a subset of mod_features

    import numpy as np
    import pandas as pd
    import math
    import datetime as dt
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    from urllib.parse import urlparse
    import os
    import psycopg2

    #import data from SQL 

    #fornow, just get data from df. 
    my_df = df 


    #list of features to be used in mod. 
    X = my_df[[mod_features]]
    cols_to_transform = ['age', 'gender', 'size','City']
    X = pd.get_dummies(X, columns = cols_to_transform )

    #fill in dummies for missing columns
    #X['age_Baby'] = 0


    #load the pickled model 
    filename = 'draft_pet_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    #get predictions for whole list of dogs 
    pred_ys = loaded_model.predict(X)
    my_df['pred_ys'] = 

    #transform pred_ys into actually useable info
    # probability, round to two places. np.around(prob_accept, 2)


    #make new predictions for a change in location 


    #return dataframe with prediction in current location, and three other cities 
    
    
    return my_df

