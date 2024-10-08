import numpy as np  # Numerical computations
import pandas as pd  # Data manipulation and analysis

# Plotting libraries
import matplotlib.pyplot as plt  # Plotting
import seaborn as sns  # Statistical data visualization

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


def Read(path):
    '''
    Read a CSV file and convert it to a pandas DataFrame.
    '''
    df = pd.read_csv(path)
    return df


def Head(df, value):
    '''
    Display the first 'value' rows of the DataFrame.
    '''
    return df.head(value)


def Tail(df, value):
    '''
    Display the last 'value' rows of the DataFrame.
    '''
    return df.tail(value)


def Shape(df):
    '''
    Return the shape (rows, columns) of the DataFrame.
    '''
    return df.shape


def Info(df):
    '''
    Display DataFrame information including column types and non-null counts.
    '''
    return df.info()


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

    return df, e


def Replace_With_NaN(df, e):
    '''
    Replace specific values in the DataFrame with NaN.
    '''
    df.replace(e, np.nan, inplace=True)
    return df


def Datatypes(df):
    '''
    Return the datatypes of all columns in the DataFrame.
    '''
    return df.dtypes


def Heatmap_For_Null_Values(df):
    '''
    Plot a heatmap to visualize missing values in the DataFrame.
    '''
    plt.figure(figsize=(8, 5))
    return sns.heatmap(df.isnull(), cbar=False)


def Value_Counts(df, column):
    '''
    Return the count of unique values in a specified column.
    '''
    return df[column].value_counts()


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
