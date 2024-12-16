
from django.http import FileResponse
from io import BytesIO
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

from num2words import num2words

from app_deploy.deploy import SelectJefeDepen

import urllib.parse
import segno

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

            print("****************** resultado ******************")
            print(resultado)
            
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

                # ciudadano_reniec = requests.get("https://ws5.pide.gob.pe/Rest/Reniec/Consultar?nuDniConsulta={}&nuDniUsuario={}&nuRucUsuario={}&password={}&out=json".format(numero, os.environ.get('RENIEC_NUDNIUSUARIO'), os.environ.get('RENIEC_NURUCUSUARIO'), os.environ.get('RENIEC_PASSWORD'))).json()
                ciudadano_reniec = requests.get("https://ws2.pide.gob.pe/Rest/RENIEC/Consultar?nuDniConsulta={}&nuDniUsuario={}&nuRucUsuario={}&password={}&out=json".format(numero, os.environ.get('RENIEC_NUDNIUSUARIO'), os.environ.get('RENIEC_NURUCUSUARIO'), os.environ.get('RENIEC_PASSWORD'))).json()
                
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
                ddp_numruc = str(contribuyente["ddp_numruc"].get("$", ""))
                ddp_nombre = str(contribuyente["ddp_nombre"].get("$", ""))
                ddp_nomzon = str(contribuyente["ddp_nomzon"].get("$", ""))
                ddp_nomvia = str(contribuyente["ddp_nomvia"].get("$", ""))
                ddp_numer1 = str(contribuyente["ddp_numer1"].get("$", ""))
                ddp_refer1 = str(contribuyente["ddp_refer1"].get("$", ""))
                desc_tipvia = str(contribuyente["desc_tipvia"].get("$", ""))
                desc_dep = str(contribuyente["desc_dep"].get("$", ""))
                desc_prov = str(contribuyente["desc_prov"].get("$", ""))
                desc_dist = str(contribuyente["desc_dist"].get("$", ""))
                desc_tpoemp = str(contribuyente["desc_tpoemp"].get("$", ""))
                desc_identi = str(contribuyente["desc_identi"].get("$", ""))
                esActivo = contribuyente["esActivo"].get("$", False)
                esHabido = contribuyente["esHabido"].get("$", False)
            
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
      

class GenerateQrImageController(RetrieveAPIView):
    
    
    def get(self, request: Request):
        data = request.query_params.get("data")
        scale = request.query_params.get("scale", 5)
        border_str = request.query_params.get("border", 1)

        border = int(border_str)

        if not data:
            return Response(data={
                "message":"Debe de ingresar data"
            }, status=status.HTTP_404_NOT_FOUND)

        # encoded_data = urllib.parse.quote(data)
        if data.startswith('http'):
            encoded_data = data.replace('%26', '&')
        else:
            encoded_data = data

        qrcode = segno.make_qr(encoded_data)

        # Crear un objeto BytesIO para almacenar la imagen del código QR
        buffer = BytesIO()

        # Guardar la imagen del código QR en el objeto BytesIO
        qrcode.save(buffer, kind='png', scale=scale, border=border)

        # Mover el cursor al inicio del objeto BytesIO
        buffer.seek(0)

        # Crear una respuesta de archivo con la imagen del código QR
        response = FileResponse(buffer, as_attachment=True, filename='qrcode.png')

        return response
    


class SelectJefeDepenController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        anio = request.query_params.get('anio')
        coddep = request.query_params.get('coddep')

        if anio and coddep:            
            jefe_depen = SelectJefeDepen(anio, coddep)

            if len(jefe_depen) == 0:
                jefe_depen = {}
            else:
                jefe_depen = jefe_depen[0]

            return Response(data={"message": None, "content": jefe_depen}, status=200)

        else:
            return Response(
                data={"message": "Debe de ingresar año y código de dependencia buscado","content": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        
def number_to_word_currency(amount):
    # Separar la parte entera y la parte decimal
    entero, decimal = str(amount).split('.')
    
    # Convertir la parte entera a palabras
    entero_texto = num2words(int(entero), lang='es')
    
    # Formatear la parte decimal
    decimal_texto = f"{int(decimal):02d}/100"
    
    # Combinar las partes en el formato deseado
    resultado = f"{entero_texto} con {decimal_texto} nuevos soles"
    
    return resultado        