import json
import os
import pandas as pd

def Read(path):
    '''
    Read a CSV file and convert it to a pandas DataFrame.
    
    '''
  
    df = pd.read_csv('uploads/'+ path)
    return df

def Columns(df):
    return df.columns