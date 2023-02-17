from django.shortcuts import render
import requests
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import LoginSerializer
from . import trabajador
from app_deploy.seguridad.usuario import login
from rest_framework.permissions import IsAuthenticated
import mimetypes
import os
from django.http.response import HttpResponse
from django.shortcuts import render# Define function to download pdf file using template
from django.conf import settings
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)

def download_file(request, filename=''):
    if filename != '':
        # Define Django project base directory
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                   
        BASE_DIR = "T:/467/"               
        # Define the full file path
        # filepath = BASE_DIR + '/app_deploy/files/' + filename
        filepath = BASE_DIR + filename
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


# Create your views here.
class SelectTrabajadorController(RetrieveAPIView):
    #serializer_class = SelectTrabajadorSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        field = request.query_params.get('field')
        valor = request.query_params.get('valor')

        if field and valor:            
            trabajador_list = trabajador.select_trabajador(field, valor)            
            return Response({'data': trabajador_list}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar campo a buscar y valor buscado"
                }, status=status.HTTP_404_NOT_FOUND)


class LoginController(RetrieveAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():            
            usuario = data.validated_data.get('usuario')
            password = data.validated_data.get('password')

            resultado = login(usuario, password)
            
            return Response({'data': resultado}, status=status.HTTP_200_OK)

        else:
            return Response(data={
                'message': 'No se pudo validar login',
                'content': data.errors
            }, status=400)

        
def downloadFileMedia(request, app='', filename=''):
    if app != '' and filename != '':        
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                   
        BASE_DIR = str(settings.MEDIA_ROOT)
        # Define the full file path
        # filepath = BASE_DIR + '/app_deploy/files/' + filename
        filepath = BASE_DIR + '/app_' +  app + '/' + filename
        # print(filepath)
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
    

class BuscarReniecDNIController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        numero = request.query_params.get('numero', '')                
        responsable = request.query_params.get('responsable', '')                

        if len(numero) == 8 and len(responsable) > 0:
            ciudadano_reniec = requests.get("https://ws5.pide.gob.pe/Rest/Reniec/Consultar?nuDniConsulta={}&nuDniUsuario={}&nuRucUsuario={}&password={}&out=json".format(numero, os.environ.get('RENIEC_NUDNIUSUARIO'), os.environ.get('RENIEC_NURUCUSUARIO'), os.environ.get('RENIEC_PASSWORD'))).json()
            
            return Response(data=ciudadano_reniec, status=status.HTTP_200_OK)        
        else:
             return Response(data={
                    "message":"Debe de ingresar DNI valido y responsable de consulta"
                }, status=status.HTTP_404_NOT_FOUND)      