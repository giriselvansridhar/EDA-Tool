import numpy as np  # Numerical computations
import pandas as pd  # Data manipulation and analysis

# Plotting libraries
import matplotlib.pyplot as plt  # Plotting
import seaborn as sns  # Statistical data visualization

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

import json
import os
import io




from django.conf import settings




def Head(df, value=5):
    '''
    done
    Display the first 'value' rows of the DataFrame.
    '''
    return df.head(value)


def Tail(df, value):
    '''
    done
    Display the last 'value' rows of the DataFrame.
    '''
    return df.tail(value)


def Shape(df):
    '''
    done
    Return the shape (rows, columns) of the DataFrame.
    '''
    return df.shape




def Info(df):
    """
    Display DataFrame information including column types and non-null counts as a DataFrame.
    """
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue().splitlines()

    # Extract relevant lines (starting after the basic info part)
    info_lines = [line.strip() for line in info_str[3:-2]]

    # Split lines into columns and create a DataFrame
    info_data = []
    for line in info_lines:
        parts = line.split()
        info_data.append(parts[:2] + [" ".join(parts[2:])])

    # Create DataFrame with appropriate column names
    info_df = pd.DataFrame(info_data, columns=["Column", "Non-Null Count", "Dtype"])
    return info_df

def Datatypes(df):
    """
    Return the data types of the columns as a DataFrame.
    """
    dtype_df = pd.DataFrame(df.dtypes, columns=['Dtype']).reset_index()
    dtype_df.columns = ['Column', 'Dtype']
    return dtype_df


def Convert_Datatype_of_the_column(df, column, datatype):
    '''
    Convert the datatype of a specified column in the DataFrame.
    Raises an error if conversion causes missing values.
    '''
    try:
        # Convert the column to the specified datatype
        df[column] = df[column].astype(datatype)

        # Check for missing values
        if df[column].isnull().any():
            missing_count = df[column].isnull().sum()
            raise ValueError(f"Conversion resulted in {missing_count} missing values in column '{column}'.")

    except Exception as e:
        raise ValueError(f"An error occurred while converting the column '{column}': {str(e)}")

    return df  # No need to return 'e' if no error occurs


def Replace_With_NaN(df, e):
    '''
    Replace specific values in the DataFrame with NaN.
    '''
    df.replace(e, np.nan, inplace=True)
    return df




def Heatmap_For_Null_Values(df):
    '''
    Plot a heatmap to visualize missing values in the DataFrame.
    '''
    plt.figure(figsize=(8, 5))
    return sns.heatmap(df.isnull(), cbar=False)


def Value_Counts(df, column_name):
    """
    Returns the value counts for a specific column as a DataFrame.
    """
    value_counts_df = df[column_name].value_counts().reset_index()
    value_counts_df.columns = [column_name, 'Count']
    return value_counts_df


def Replace_By_Values(df, column, original_value, replace_value):
    '''
    Replace a specific value in a column with a new value.
    '''
    df[column].replace(original_value, replace_value, inplace=True)
    return df


def Replace_with_Mean(df, column, replace_with, datatype):
    '''
    Replace specific values in a column with the column mean.
    '''
    avg_value = df[column].astype(datatype).mean()
    df[column].replace(replace_with, avg_value, inplace=True)
    return df


def Replace_with_Mode(df, column, replace_with, datatype):
    '''
    Replace specific values in a column with the column mode.
    '''
    mode_value = df[column].astype(datatype).mode()[0]
    df[column].replace(replace_with, mode_value, inplace=True)
    return df


def Replace_with_Median(df, column, replace_with, datatype):
    '''
    Replace specific values in a column with the column median.
    '''
    median_value = df[column].astype(datatype).median()
    df[column].replace(replace_with, median_value, inplace=True)
    return df


def apply_one_hot_encoding(df, columns, drop_first=True):
    '''
    Apply one-hot encoding to the specified categorical columns in the DataFrame.
    '''
    df_encoded = pd.get_dummies(df, columns=columns, drop_first=drop_first)
    return df_encoded


def drop_column_and_display(df, column_name, num_rows=10):
    '''
    Drop a specified column from the DataFrame and display the first few rows.
    '''
    df = df.drop(column_name, axis=1)
    print(df.head(num_rows))
    return df



def load_json_file():
    folder = os.path.join(settings.MEDIA_ROOT, 'uploads/')
    file_path = os.path.join(folder, f"main.json")
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
    return data