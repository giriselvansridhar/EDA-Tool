from django.shortcuts import render, redirect
from Functions import Notes
from operation.uploads.upload import Read, Columns
import pandas as pd

# Load initial data
B = Notes.load_json_file()
FileName = B['full_name_with_extension']
Dataframe = Read(path=FileName)
Columns_Of_Dataframe = Columns(Dataframe)

def get_head_or_tail(dataframe, operation_type, value):
    """
    Helper function to return the head or tail of the dataframe.
    """
    try:
        value = int(value)
    except ValueError:
        return "Invalid value. Please provide a valid integer."

    if operation_type == "head":
        return Notes.Head(dataframe, value)
    elif operation_type == "tail":
        return Notes.Tail(dataframe, value)
    
    return None

def add_observation(session, observation_input):
    """
    Adds an observation to the session.
    """
    if 'observations' not in session:
        session['observations'] = []
    
    session['observations'].append(observation_input)
    session.modified = True  # Ensures session is saved after modification
def handle_operation(request, dataframe, operation_type, value=None, column_name=None, new_datatype=None):
    """
    Handle different operations like head, tail, shape, info, datatypes, value counts, and datatype conversion.
    """
    if operation_type in ['head', 'tail']:
        data = get_head_or_tail(dataframe, operation_type, value or 5)
    elif operation_type == 'shape':
        data = Notes.Shape(dataframe)
    elif operation_type == 'info':
        data = Notes.Info(dataframe)  # Ensure it returns a DataFrame
    elif operation_type == 'datatypes':
        data = Notes.Datatypes(dataframe)  # Ensure it returns a DataFrame
    elif operation_type == 'count' and column_name:
        if column_name in Columns_Of_Dataframe:
            data = Notes.Value_Counts(dataframe, column_name)
        else:
            return f"Invalid column: '{column_name}'. Available columns: {', '.join(Columns_Of_Dataframe)}"
    elif operation_type == 'convert_dtype' and column_name and new_datatype:
        try:
            # Perform the datatype conversion
            updated_df, error = Notes.Convert_Datatype_of_the_column(dataframe, column_name, new_datatype)
            data = f"Successfully converted column '{column_name}' to {new_datatype}."
        except ValueError as e:
            data = str(e)
    else:
        return None

    # Convert DataFrame to HTML if applicable
    if isinstance(data, pd.DataFrame):
        return data.to_html(classes='table table-striped table-bordered', index=False)
    
    return str(data)

def Operation(request):
    # Ensure 'session_data' and 'button_count' are initialized in the session
    request.session.setdefault('button_count', 0)
    request.session.setdefault('session_data', {})

    current_session_key = f"operation_{request.session['button_count']}"  # Default session key

    if request.method == "POST":
        session_data = request.session['session_data']

        # Handling different form inputs
        head_value = request.POST.get('head_value')
        tail_value = request.POST.get('tail_value')
        count_columns = request.POST.get('count_columns')
        datatype_column = request.POST.get('datatype_column')
        new_datatype = request.POST.get('new_datatype')
        
        tab_button = request.POST.get('tab_button')
        observation_input = request.POST.get('add_observation_input')

        # Handle switching between tabs (buttons)
        if tab_button:
            current_session_key = f"operation_{tab_button}"

            if tab_button in session_data:
                request.session['button_count'] = int(tab_button)
                request.session.modified = True

        operation_result = None

        # Perform dataframe operations and update session data
        operations = {
            'head': ('head', head_value),
            'tail': ('tail', tail_value),
            'shape': ('shape', None),
            'info': ('info', None),
            'datatypes': ('datatypes', None),
            'count': ('count', None, count_columns),
            'convert_dtype': ('convert_dtype', None, datatype_column, new_datatype)
        }

        for operation_key, params in operations.items():
            if request.POST.get(operation_key) == operation_key:
                operation_result = handle_operation(request, Dataframe, *params)
                if operation_result:
                    if current_session_key not in session_data:
                        session_data[current_session_key] = {'data': []}
                    session_data[current_session_key]['data'].append(operation_result)
                    request.session.modified = True

        # Handle observation input
        if observation_input:
            add_observation(request.session, observation_input)
            request.session['button_count'] += 1
            current_session_key = f"operation_{request.session['button_count']}"
            session_data[current_session_key] = {'data': []}
            request.session.modified = True

    # Pass the result to the template, including observations and the currently selected tab's data
    context = {
        'column_list': Columns_Of_Dataframe,
        'observations': request.session.get('observations', []),
        'button_count': request.session['button_count'],
        'result_list': request.session['session_data'].get(current_session_key, {}).get('data', []),
        'data_types': ['int64', 'float64', 'object', 'datetime64', 'bool']  # List of data types to choose from
    }

    return render(request, 'operation/operation.html', context)