
Libraries required for the EDA
```
pip install numpy
pip install pandas
pip install matplotlib seaborn scikit-learn
```



## 1. Import Libraries

```python
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import seaborn as sns  
import warnings
warnings.filterwarnings("ignore")
```

- **numpy**: Useful for numerical computations.
- **pandas**: Core library for data manipulation and analysis.
- **matplotlib**: A library used for creating static, animated, and interactive visualizations.
- **seaborn**: Built on top of matplotlib, used for statistical data visualization.
- **warnings**: Suppresses warnings to keep the output clean.

---

## 2. `Read(path)`

**Description**:  
This function reads a CSV file and converts it into a pandas DataFrame.

**Parameters**:
- `path` (string): The file path of the CSV file.

**Returns**:
- `df` (DataFrame): The DataFrame containing the loaded CSV data.

**Example**:
```python
df = Read("data.csv")
```

---

## 3. `Head(df, value)`

**Description**:  
Displays the first 'n' rows of a DataFrame.

**Parameters**:
- `df` (DataFrame): The DataFrame to inspect.
- `value` (int): The number of rows to display.

**Returns**:
- DataFrame: The first 'value' rows of the DataFrame.

**Example**:
```python
print(Head(df, 5))
```

---

## 4. `Tail(df, value)`

**Description**:  
Displays the last 'n' rows of a DataFrame.

**Parameters**:
- `df` (DataFrame): The DataFrame to inspect.
- `value` (int): The number of rows to display.

**Returns**:
- DataFrame: The last 'value' rows of the DataFrame.

**Example**:
```python
print(Tail(df, 5))
```

---

## 5. `Shape(df)`

**Description**:  
Returns the shape (number of rows and columns) of the DataFrame.

**Parameters**:
- `df` (DataFrame): The DataFrame whose shape you want to inspect.

**Returns**:
- `tuple`: The shape of the DataFrame in the format (rows, columns).

**Example**:
```python
print(Shape(df))
```

---

## 6. `Info(df)`

**Description**:  
Displays concise summary information about the DataFrame, such as column names, non-null counts, and datatypes.

**Parameters**:
- `df` (DataFrame): The DataFrame whose information is to be displayed.

**Returns**:
- Prints information about the DataFrame.

**Example**:
```python
Info(df)
```

---

## 7. `Convert_Datatype_of_the_column(df, column, datatype)`

**Description**:  
Converts the datatype of a specified column in the DataFrame. Raises an error if conversion causes missing values.

**Parameters**:
- `df` (DataFrame): The DataFrame containing the column to be converted.
- `column` (string): The name of the column whose datatype will be changed.
- `datatype` (type): The target datatype (e.g., `float`, `int`).

**Returns**:
- `df` (DataFrame): The updated DataFrame.
- `e` (Exception, if any): The exception encountered during conversion.

**Example**:
```python
df, e = Convert_Datatype_of_the_column(df, 'age', int)
```

---

## 8. `Replace_With_NaN(df, e)`

**Description**:  
Replaces specific values in the DataFrame with `NaN`.

**Parameters**:
- `df` (DataFrame): The DataFrame where values need to be replaced.
- `e`: The value to replace with `NaN`.

**Returns**:
- `df` (DataFrame): The DataFrame with replaced values.

**Example**:
```python
df = Replace_With_NaN(df, e)
```

---

## 9. `Datatypes(df)`

**Description**:  
Returns the datatypes of all columns in the DataFrame.

**Parameters**:
- `df` (DataFrame): The DataFrame to inspect.

**Returns**:
- `Series`: Data types of each column.

**Example**:
```python
print(Datatypes(df))
```

---

## 10. `Heatmap_For_Null_Values(df)`

**Description**:  
Plots a heatmap that visualizes missing values in the DataFrame.

**Parameters**:
- `df` (DataFrame): The DataFrame to visualize.

**Returns**:
- `seaborn.heatmap`: A heatmap plot indicating missing values.

**Example**:
```python
Heatmap_For_Null_Values(df)
```

---

## 11. `Value_Counts(df, column)`

**Description**:  
Returns the count of unique values in a specified column.

**Parameters**:
- `df` (DataFrame): The DataFrame to analyze.
- `column` (string): The column to count unique values in.

**Returns**:
- `Series`: The counts of unique values.

**Example**:
```python
print(Value_Counts(df, 'age'))
```

---

## 12. `Replace_By_Values(df, column, original_value, replace_value)`

**Description**:  
Replaces a specific value in a column with another value.

**Parameters**:
- `df` (DataFrame): The DataFrame to modify.
- `column` (string): The column to search for the original value.
- `original_value`: The value to be replaced.
- `replace_value`: The value to replace it with.

**Returns**:
- `df` (DataFrame): The updated DataFrame.

**Example**:
```python
df = Replace_By_Values(df, 'age', 0, np.nan)
```

---

## 13. `Replace_with_Mean(df, column, replace_with, datatype)`

**Description**:  
Replaces a specific value in a column with the column mean.

**Parameters**:
- `df` (DataFrame): The DataFrame to modify.
- `column` (string): The column to modify.
- `replace_with`: The value to replace.
- `datatype` (type): The datatype of the column.

**Returns**:
- `df` (DataFrame): The updated DataFrame.

**Example**:
```python
df = Replace_with_Mean(df, 'age', np.nan, float)
```

---

## 14. `Replace_with_Mode(df, column, replace_with, datatype)`

**Description**:  
Replaces a specific value in a column with the column mode.

**Parameters**:
- `df` (DataFrame): The DataFrame to modify.
- `column` (string): The column to modify.
- `replace_with`: The value to replace.
- `datatype` (type): The datatype of the column.

**Returns**:
- `df` (DataFrame): The updated DataFrame.

**Example**:
```python
df = Replace_with_Mode(df, 'age', np.nan, float)
```

---

## 15. `Replace_with_Median(df, column, replace_with, datatype)`

**Description**:  
Replaces a specific value in a column with the column median.

**Parameters**:
- `df` (DataFrame): The DataFrame to modify.
- `column` (string): The column to modify.
- `replace_with`: The value to replace.
- `datatype` (type): The datatype of the column.

**Returns**:
- `df` (DataFrame): The updated DataFrame.

**Example**:
```python
df = Replace_with_Median(df, 'age', np.nan, float)
```

---

## 16. `apply_one_hot_encoding(df, columns, drop_first=True)`

**Description**:  
Applies one-hot encoding to the specified categorical columns.

**Parameters**:
- `df` (DataFrame): The DataFrame to encode.
- `columns` (list): List of categorical columns to encode.
- `drop_first` (bool, optional): Whether to drop the first category to avoid multicollinearity (default is `True`).

**Returns**:
- `df_encoded` (DataFrame): The DataFrame with one-hot encoded columns.

**Example**:
```python
df_encoded = apply_one_hot_encoding(df, ['gender', 'city'])
```

---

## 17. `drop_column_and_display(df, column_name, num_rows=10)`

**Description**:  
Drops a specified column from the DataFrame and displays the first few rows of the updated DataFrame.

**Parameters**:
- `df` (DataFrame): The DataFrame to modify.
- `column_name` (string): The column to drop.
- `num_rows` (int, optional): Number of rows to display after dropping (default is 10).

**Returns**:
- `df` (DataFrame): The DataFrame with the column removed.

**Example**:
```python
df = drop_column_and_display(df, 'age')
```


