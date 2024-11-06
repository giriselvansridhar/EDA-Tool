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
def handle_operation(request, dataframe, operation_type, value=None, column_name=None, original_value=None, replace_value=None, datatype=None):
    """
    Handle different operations like head, tail, shape, info, datatypes, value counts, and replacements.
    """
    if operation_type in ['head', 'tail']:
        data = get_head_or_tail(dataframe, operation_type, value or 5)
    elif operation_type == 'shape':
        data = Notes.Shape(dataframe)
    elif operation_type == 'info':
        data = Notes.Info(dataframe)
    elif operation_type == 'datatypes':
        data = Notes.Datatypes(dataframe)
    elif operation_type == 'count' and column_name:
        if column_name in Columns_Of_Dataframe:
            data = Notes.Value_Counts(dataframe, column_name)
        else:
            return f"Invalid column: '{column_name}'. Available columns: {', '.join(Columns_Of_Dataframe)}"
    
    # Handle replacement operations
    elif operation_type == 'replace_nan':
        dataframe = Notes.Replace_With_NaN(dataframe, value)
        data = f"Replaced '{value}' with NaN."
    elif operation_type == 'replace_value' and column_name and original_value is not None and replace_value is not None:
        dataframe = Notes.Replace_By_Values(dataframe, column_name, original_value, replace_value)
        data = f"Replaced '{original_value}' with '{replace_value}' in column '{column_name}'."
    elif operation_type == 'replace_mean' and column_name and datatype:
        dataframe = Notes.Replace_with_Mean(dataframe, column_name, value, datatype)
        data = f"Replaced '{value}' with mean in column '{column_name}'."
    elif operation_type == 'replace_mode' and column_name and datatype:
        dataframe = Notes.Replace_with_Mode(dataframe, column_name, value, datatype)
        data = f"Replaced '{value}' with mode in column '{column_name}'."
    elif operation_type == 'replace_median' and column_name and datatype:
        dataframe = NotesReplace_with_Median(dataframe, column_name, value, datatype)
        data = f"Replaced '{value}' with median in column '{column_name}'."
    else:
        return None
    
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

        # Inputs for replacement
        original_value = request.POST.get('original_value')
        replace_value = request.POST.get('replace_value')
        column_name = request.POST.get('column')
        replace_nan_value = request.POST.get('replace_nan_value')
        new_datatype = request.POST.get('datatype')

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
        if request.POST.get('head') == 'head':
            operation_result = handle_operation(request, Dataframe, 'head', head_value)
        elif request.POST.get('tail') == 'tail':
            operation_result = handle_operation(request, Dataframe, 'tail', tail_value)
        elif request.POST.get('shape') == 'shape':
            operation_result = handle_operation(request, Dataframe, 'shape')
        elif request.POST.get('info') == 'info':
            operation_result = handle_operation(request, Dataframe, 'info')
        elif request.POST.get('datatypes') == 'datatypes':
            operation_result = handle_operation(request, Dataframe, 'datatypes')
        elif request.POST.get('count') == 'count' and count_columns:
            operation_result = handle_operation(request, Dataframe, 'count', column_name=count_columns)
        elif request.POST.get('replace_nan') == 'replace_nan':
            operation_result = handle_operation(request, Dataframe, 'replace_nan', value=replace_nan_value)
        elif request.POST.get('replace_value') == 'replace_value':
            operation_result = handle_operation(request, Dataframe, 'replace_value', column_name=column_name, original_value=original_value, replace_value=replace_value)
        elif request.POST.get('replace_mean') == 'replace_mean':
            operation_result = handle_operation(request, Dataframe, 'replace_mean', column_name=column_name, datatype=new_datatype)
        elif request.POST.get('replace_mode') == 'replace_mode':
            operation_result = handle_operation(request, Dataframe, 'replace_mode', column_name=column_name, datatype=new_datatype)
        elif request.POST.get('replace_median') == 'replace_median':
            operation_result = handle_operation(request, Dataframe, 'replace_median', column_name=column_name, datatype=new_datatype)

        if operation_result:
            if current_session_key not in session_data:
                session_data[current_session_key] = {'data': []}
            session_data[current_session_key]['data'].append(operation_result)
            request.session.modified = True

        if observation_input:
            add_observation(request.session, observation_input)
            request.session['button_count'] += 1
            current_session_key = f"operation_{request.session['button_count']}"
            session_data[current_session_key] = {'data': []}
            request.session.modified = True

    context = {
        'column_list': Columns_Of_Dataframe,
        'observations': request.session.get('observations', []),
        'button_count': request.session['button_count'],
        'result_list': request.session['session_data'].get(current_session_key, {}).get('data', [])
    }

    return render(request, 'operation/operation.html', context)

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

        # Inputs for replacement
        original_value = request.POST.get('original_value')
        replace_value = request.POST.get('replace_value')
        column_name = request.POST.get('column')
        replace_nan_value = request.POST.get('replace_nan_value')
        new_datatype = request.POST.get('datatype')
        replace_value_type = request.POST.get('replace_value_type')

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
            'replace_nan': ('replace_nan', replace_nan_value),
            'replace_value': ('replace_value', None, column_name, original_value, replace_value),
            'replace_mean': ('replace_mean', None, column_name, None, new_datatype),
            'replace_mode': ('replace_mode', None, column_name, None, new_datatype),
            'replace_median': ('replace_median', None, column_name, None, new_datatype)
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
        'result_list': request.session['session_data'].get(current_session_key, {}).get('data', [])
    }

    return render(request, 'operation/operation.html', context)

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

    context = {
    'column_list': Columns_Of_Dataframe,
    'observations': request.session.get('observations', []),
    'button_count': request.session['button_count'],
    'result_list': request.session['session_data'].get(current_session_key, {}).get('data', []),
    'data_types': ['int64', 'float64', 'object', 'datetime64', 'bool'],  # Ensure this is passed
    'selected_dtype': request.POST.get('new_datatype', '')  # Retrieve the selected datatype from POST request
}

    return render(request, 'operation/operation.html', context)


    # Pass the result to the template, including observations and the currently selected tab's data



