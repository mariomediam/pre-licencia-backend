import os
import mimetypes
from django.http.response import HttpResponse
from django.shortcuts import render# Define function to download pdf file using template
from os import environ
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)

def download_file(request, filename=''):
    if filename != '':
        # Define Django project base directory
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                   
        BASE_DIR = environ.get('RUTA_REQUISITOS_LICENCIA')            
        # Define the full file path
        filepath = BASE_DIR + filename
        # filepath = BASE_DIR + filename
        print(filepath)
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'file.html')

