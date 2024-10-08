from django.shortcuts import render, redirect
from .forms import UploadFileForm
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import json

def Homepage(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            folder = os.path.join(settings.MEDIA_ROOT, 'uploads/')
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            # Save the uploaded file to the 'uploads/' folder
            fs = FileSystemStorage(location=folder)
            filename = fs.save(uploaded_file.name, uploaded_file)
            
            # Get the full path of the saved file
            file_path = os.path.join(folder, filename)

            # (Optional) Print the file path for debugging purposes
            print(f"File saved at: {file_path}")

            # Create a JSON file with the name, extension, and full file name
            json_data = {
                "file_name": os.path.splitext(uploaded_file.name)[0],  # File name without extension
                "extension": os.path.splitext(uploaded_file.name)[1],   # File extension
                "full_name_with_extension": uploaded_file.name          # Full file name with extension
            }

            # Define the JSON file path
            json_file_path = os.path.join(folder, f"main.json")

            # Write JSON data to the file
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)

            print(f"JSON file created at: {json_file_path}")

            # Call your processing function with the file path
            
            # Redirect to the 'operations/' page after successful upload and JSON creation
            return redirect('operations/')
    
    else:
        form = UploadFileForm()

    # Render the homepage with the file upload form
    return render(request, 'homepage/homepage.html', {'form': form})