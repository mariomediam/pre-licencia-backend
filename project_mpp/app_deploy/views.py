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
from .general.consultasReniec import AgregarConsultaReniec, ValidaAccesoConsultaReniec

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
        responsable = request.user.username

        valida_acceso = ValidaAccesoConsultaReniec(responsable)
        if valida_acceso["acceso"] == True:

            if len(numero) == 8 and len(responsable) > 0:
                ap_primer = None
                ap_segundo = None
                direccion = None
                estado_civil = None
                foto = None
                pre_nombres = None
                restriccion = None
                ubigeo = None

                ciudadano_reniec = requests.get("https://ws5.pide.gob.pe/Rest/Reniec/Consultar?nuDniConsulta={}&nuDniUsuario={}&nuRucUsuario={}&password={}&out=json".format(numero, os.environ.get('RENIEC_NUDNIUSUARIO'), os.environ.get('RENIEC_NURUCUSUARIO'), os.environ.get('RENIEC_PASSWORD'))).json()
                
                co_resultado = ciudadano_reniec["consultarResponse"]["return"]["coResultado"]    

                if (co_resultado == "0000"):
                    datos_persona = ciudadano_reniec["consultarResponse"]["return"]["datosPersona"]                
                    ap_primer = datos_persona["apPrimer"]                
                    ap_segundo = datos_persona["apSegundo"]
                    direccion = datos_persona["direccion"]
                    estado_civil = datos_persona["estadoCivil"]
                    foto = datos_persona["foto"]
                    pre_nombres = datos_persona["prenombres"]
                    restriccion = datos_persona["restriccion"]
                    ubigeo = datos_persona["ubigeo"]
                
                de_resultado = ciudadano_reniec["consultarResponse"]["return"]["deResultado"]

                AgregarConsultaReniec(responsable, numero, co_resultado, ap_primer, ap_segundo, direccion, estado_civil, foto, pre_nombres,restriccion, ubigeo, de_resultado)
                
                return Response(data=ciudadano_reniec, status=status.HTTP_200_OK)        
            else:
                return Response(data={
                        "message":"Debe de ingresar DNI valido y responsable de consulta"
                    }, status=status.HTTP_404_NOT_FOUND) 
        else:
                return Response(data={
                        "message":"No tiene acceso para realizar consultas a RENIEC"
                    }, status=status.HTTP_404_NOT_FOUND)     
        
class BuscarSunatRUCController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        numero = request.query_params.get('numero', '')                
        responsable = request.user.username

        if len(numero) == 11 and len(responsable) > 0:
            # ap_primer = None
            # ap_segundo = None
            # direccion = None
            # estado_civil = None
            # foto = None
            # pre_nombres = None
            # restriccion = None
            # ubigeo = None

            data_contribuyente = requests.get("https://ws3.pide.gob.pe/Rest/Sunat/DatosPrincipales?numruc={}&out=json".format(numero)).json()
            contribuyente = data_contribuyente["list"]["multiRef"]

            existe = False
            ddp_numruc = ""
            ddp_nombre = ""
            ddp_nomzon = ""
            ddp_nomvia = ""
            ddp_numer1 = ""
            ddp_refer1 = ""
            desc_tipvia = ""
            desc_dep = ""
            desc_prov = ""
            desc_dist = ""
            desc_tpoemp = ""
            desc_identi = ""
            esActivo = False
            esHabido = False

            if "$" in contribuyente["ddp_numruc"]: 
                existe = True           
                ddp_numruc = contribuyente["ddp_numruc"]["$"]
                ddp_nombre = contribuyente["ddp_nombre"]["$"]
                ddp_nomzon = contribuyente["ddp_nomzon"]["$"]
                ddp_nomvia = contribuyente["ddp_nomvia"]["$"]
                ddp_numer1 = contribuyente["ddp_numer1"]["$"]
                ddp_refer1 = contribuyente["ddp_refer1"]["$"]
                desc_tipvia = contribuyente["desc_tipvia"]["$"]
                desc_dep = contribuyente["desc_dep"]["$"]
                desc_prov = contribuyente["desc_prov"]["$"]
                desc_dist = contribuyente["desc_dist"]["$"]
                desc_tpoemp = contribuyente["desc_tpoemp"]["$"]
                desc_identi = contribuyente["desc_identi"]["$"]
                esActivo = contribuyente["esActivo"]["$"]
                esHabido = contribuyente["esHabido"]["$"]
            
            contribuyente_json = {
                "existe" : existe,
                "ddp_numruc" : ddp_numruc,
                "ddp_nombre" : ddp_nombre,
                "ddp_nomzon" : ddp_nomzon,
                "ddp_nomvia" : ddp_nomvia,
                "ddp_numer1" : ddp_numer1,
                "ddp_refer1" : ddp_refer1,
                "desc_tipvia" : desc_tipvia,
                "desc_dep" : desc_dep,
                "desc_prov" : desc_prov,
                "desc_dist" : desc_dist,
                "desc_tpoemp" : desc_tpoemp,
                "desc_identi" : desc_identi,
                "esActivo" : esActivo,
                "esHabido" : esHabido
            }
            
            return Response(data=contribuyente_json, status=status.HTTP_200_OK)        
        else:
            return Response(data={
                    "message":"Debe de ingresar RUC valido y responsable de consulta"
                }, status=status.HTTP_404_NOT_FOUND) 
      