import os
from os import environ

from django.shortcuts import render
from django.template.loader import get_template

from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from dotenv import load_dotenv

from app_rrhh.rrhh import ListaPlanillaDetalle, SelectPlanillaBoleta

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


import pdfkit

# Create your views here.

class GenerateBoletasPdfController(UpdateAPIView):    
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        
        anio = request.data.get('anio')
        mes = request.data.get('mes')
        tipo = request.data.get('tipo')
        numero = request.data.get('numero')
        dni = request.data.get('dni')
        n_user = request.user.username
        c_banco_id = request.data.get('c_banco_id')

        if anio and mes and tipo and numero and dni and n_user:

            boleta_pago = ListaPlanillaDetalle(anio, mes, tipo, numero, dni, n_user, c_banco_id)

            if len(boleta_pago) > 0:

                data = {"testUserId" : boleta_pago[0]["c_traba_dni"], "testUserName" : boleta_pago[0]["n_nombre"]}      
                template = get_template('boleta.html')
                html = template.render(data)

                BASE_DIR = environ.get('RUTA_BOLETAS_PAGO')
                
                # CREA DIRECTORIO 2023
                # if not os.path.exists(BASE_DIR + '2023'):
                #     os.mkdir(BASE_DIR + '2023')
                
                file_path = BASE_DIR + 'boleta.pdf'
                pdfkit.from_string(html, file_path)
            
                return Response(data={
                    "message":"Boleta generada con exito"
                    }, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    "message":"No se encontraron datos"
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                "message":"Error al generar boleta"
                }, status=status.HTTP_400_BAD_REQUEST)  
        

# Create your views here.
class SelectPlanillaBoletaController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        anio = request.query_params.get('anio')
        mes = request.query_params.get('mes')

        if anio and mes:            
            planillas = SelectPlanillaBoleta(anio, mes)
            
            return Response(data = {
            "message":None,
            "content":planillas
            }, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar año y mes a consultar"
                }, status=status.HTTP_404_NOT_FOUND)        