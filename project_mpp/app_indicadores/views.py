from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from app_indicadores.indicadores import BuscarRecaudacionSATP

# Create your views here.
class BuscarRecaudacionSATPController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        anio = request.query_params.get('anio')
        mes = request.query_params.get('mes')
        tasas = request.query_params.get('tasas')

        if not anio or not mes or not tasas:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)


        return Response(data={
            "message": "Recaudación obtenida correctamente",
            "content": [
        {
            "Tasa": "307",
            "Mes": 1,
            "Monto": 301.75
        },
        {
            "Tasa": "307",
            "Mes": 2,
            "Monto": 230.75
        },
        {
            "Tasa": "307",
            "Mes": 3,
            "Monto": 195.25
        },
        {
            "Tasa": "307",
            "Mes": 4,
            "Monto": 408.25
        },
        {
            "Tasa": "307",
            "Mes": 5,
            "Monto": 372.75
        },
        {
            "Tasa": "307",
            "Mes": 6,
            "Monto": 497.0
        },
        {
            "Tasa": "307",
            "Mes": 7,
            "Monto": 461.5
        },
        {
            "Tasa": "307",
            "Mes": 8,
            "Monto": 852.0
        },
        {
            "Tasa": "307",
            "Mes": 9,
            "Monto": 1420.0
        },
        {
            "Tasa": "307",
            "Mes": 10,
            "Monto": 1136.0
        },
        {
            "Tasa": "307",
            "Mes": 11,
            "Monto": 923.0
        },
        {
            "Tasa": "307",
            "Mes": 12,
            "Monto": 443.75
        },
        {
            "Tasa": "334",
            "Mes": 2,
            "Monto": 48.3
        },
        {
            "Tasa": "334",
            "Mes": 4,
            "Monto": 144.9
        },
        {
            "Tasa": "334",
            "Mes": 7,
            "Monto": 96.6
        },
        {
            "Tasa": "334",
            "Mes": 9,
            "Monto": 193.2
        },
        {
            "Tasa": "334",
            "Mes": 11,
            "Monto": 48.3
        }
        ]
            }, status=status.HTTP_200_OK)


        recaudacion = BuscarRecaudacionSATP(anio, mes, tasas)

        return Response(data={
            "message": "Recaudación obtenida correctamente",
            "content": recaudacion
        }, status=status.HTTP_200_OK)


