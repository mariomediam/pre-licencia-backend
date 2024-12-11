from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

# Create your views here.

from .transporte import *

class TransporteVigenteView(RetrieveAPIView):

    def get(self, request: Request):        
        data = S09TranspVigente()

        return Response(
            data={"message": "Lista de transportes vigentes", "content": data},
            status=status.HTTP_200_OK,
        )

class TranspxAnioView(RetrieveAPIView):

    def get(self, request: Request):        
        c_anio = request.query_params.get("anio")
        data = S09TranspxAnio(c_anio)

        return Response(
            data={"message": "Vehiculos autorizados", "content": data},
            status=status.HTTP_200_OK,
        )

class ComparaTranspxAnioView(RetrieveAPIView):

    def get(self, request: Request):        
        m_dia = request.query_params.get("dia")
        m_mes = request.query_params.get("mes")
        c_anio01 = request.query_params.get("anio01")
        c_anio02 = request.query_params.get("anio02")
        opcion = request.query_params.get("opcion", 1)

        opcion = int(opcion)

        if opcion == 1 and (m_dia ==None or m_mes == None or c_anio01 == None or c_anio02 == None):
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        data = S09ComparaTranspxAnio(m_dia, m_mes, c_anio01, c_anio02, opcion)        

        return Response(
            data={"message": "Comparacion de vehiculos autorizados", "content": data},
            status=status.HTTP_200_OK,
        )
    
class TranspxAnioyMesView(RetrieveAPIView):

    def get(self, request: Request):        
        c_anio = request.query_params.get("anio")
        data = S09TranspxAnioyMes(c_anio)

        return Response(
            data={"message": "Vehiculos autorizados por mes", "content": data},
            status=status.HTTP_200_OK,
        )

class InfraccionesTransportexAnioView(RetrieveAPIView):
    
    def get(self, request: Request):        
        c_anio = request.query_params.get("anio")    
        
        data = S05InfraccionesTransportexAnio(c_anio)

        return Response(
            data={"message": "Infracciones de transporte", "content": data},
            status=status.HTTP_200_OK,
        )
        
class ComparaInfraccTransportexAnioView(RetrieveAPIView):

    def get(self, request: Request):        
        m_dia = request.query_params.get("dia")
        m_mes = request.query_params.get("mes")
        c_anio01 = request.query_params.get("anio01")
        c_anio02 = request.query_params.get("anio02")

        if m_dia ==None or m_mes == None or c_anio01 == None or c_anio02 == None:
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        data = S05ComparaInfraccTransportexAnio(m_dia, m_mes, c_anio01, c_anio02)

        return Response(
            data={"message": "Comparacion de infracciones de transporte", "content": data},
            status=status.HTTP_200_OK,
        ) 

class TranspAntigVehicView(RetrieveAPIView):

    def get(self, request: Request):        
        
        
        data = S09TranspAntigVehic()

        return Response(
            data={"message": "Vehiculos antiguos", "content": data},
            status=status.HTTP_200_OK,
        )
    
class OcurrenciasxAnioView(RetrieveAPIView):
    
        def get(self, request: Request):        
            c_opcion = request.query_params.get("opcion")
            c_anio = request.query_params.get("anio")
    
            if c_opcion == None or c_anio == None:
                return Response(
                    data={"message": "Faltan parametros"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            data = S09OcurrenciasxAnio(c_opcion, c_anio)
    
            return Response(
                data={"message": "Ocurrencias por año", "content": data},
                status=status.HTTP_200_OK,
            )
        
class MontosPapeletaTransitoView(RetrieveAPIView):
    
        def get(self, request: Request):        
            anio = request.query_params.get("anio")
            tipo_infraccion = request.query_params.get("tipo")
            mes = request.query_params.get("mes")
    
            if anio == None or tipo_infraccion == None:
                return Response(
                    data={"message": "Faltan parametros"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            data = S09MontosPapeletaTransito(anio, tipo_infraccion, mes)
    
            return Response(
                data={"message": "Montos de papeletas de transito", "content": data},
                status=status.HTTP_200_OK,
            )
        
class ComparaMontosPapeletaTransitoView(RetrieveAPIView):
    
        def get(self, request: Request):        
            m_dia = request.query_params.get("dia")
            m_mes = request.query_params.get("mes")
            c_anio01 = request.query_params.get("anio01")
            c_anio02 = request.query_params.get("anio02")
    
            if m_dia ==None or m_mes == None or c_anio01 == None or c_anio02 == None:
                return Response(
                    data={"message": "Faltan parametros"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            data = S05ComparaMontosPapeletaTransito(m_dia, m_mes, c_anio01, c_anio02)
    
            return Response(
                data={"message": "Comparacion de montos de papeletas de transito", "content": data},
                status=status.HTTP_200_OK,
            )