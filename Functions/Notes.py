# Import necessary libraries
import numpy as np  # Numerical computations
import pandas as pd  # Data manipulation and analysis

# Plotting libraries
import matplotlib.pyplot as plt  # Plotting
import seaborn as sns  # Statistical data visualization

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Print a confirmation message
print("All libraries are imported")

# Encoding libraries
from sklearn.preprocessing import OneHotEncoder  # Converts categorical data into binary vectors
from sklearn.preprocessing import LabelEncoder  # Encodes categorical data as numeric labels
from sklearn.preprocessing import OrdinalEncoder  # Encodes ordinal categorical features

# Feature scaling libraries
from sklearn.preprocessing import StandardScaler  # Z-score normalization
from sklearn.preprocessing import MinMaxScaler  # Min-Max scaling


def Read(path):
    '''
    Read a file and convvert to the dataframe with the pandas dataframe
    
    
    '''
    df=pd.read_csv(path)
    return df

def Head(df,Value):

    '''
    Find the Head of the dataframe
    '''
    return df.head(Value)

def Tail(df,Value):
    '''
    Find the last tail of the dataframe '''
    return df.tail(Value)

def Shape(df):
    '''
    Find the shape of the dataframe
    '''
    return df.shape

def Info(df):
    '''
    Find the information of the dataframe

    '''
    return df.info()

def Convert_Datype_of_the_column(df,)



