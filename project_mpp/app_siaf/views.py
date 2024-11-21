from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .siaf import *

# Create your views here.
class MaestroDocumentoView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        data = sf_listar_maestro_documento()
        return Response(
            data={"message": "Lista de documentos", "content": data},
            status=status.HTTP_200_OK,
        )
    
class PersonaView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):        
        filtro = request.data.get("filtro")
        if not filtro:
            return Response(
                data={"message": "Filtro no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        data = sf_seleccionar_persona(filtro)        
        return Response(
            data={"message": "Lista de personas", "content": data},
            status=status.HTTP_200_OK,
        )
    

class ProveedorSIGAView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):        
        filtro = request.data.get("filtro")
        if not filtro:
            return Response(
                data={"message": "Filtro no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        data = sf_seleccionar_proveedor(filtro)        
        return Response(
            data={"message": "Lista de proveedores SIGA", "content": data},
            status=status.HTTP_200_OK,
        )
    

class SeleccionarExpedienteFase(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        ano_eje = request.query_params.get("ano_eje")
        expediente = request.query_params.get("expediente")
        ciclo = request.query_params.get("ciclo")
        fase = request.query_params.get("fase")

        filters = {
            "ano_eje": ano_eje,
            "expediente": expediente,
            "ciclo": ciclo,
            "fase": fase,
        }

        if not ano_eje or not expediente or not ciclo or not fase:
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        data = sf_seleccionar_expediente_fase(**filters)        
        return Response(
            data={"message": "Expediente fase", "content": data},
            status=status.HTTP_200_OK,
        )