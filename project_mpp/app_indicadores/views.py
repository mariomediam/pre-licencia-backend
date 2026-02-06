from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from app_indicadores.indicadores import BuscarRecaudacionSATP, S42SelectRecaudacionPorAnioyDependencia, S42SelectProyeccionPorAnioyDependencia, S42SelectRecaudacionPorAnioyTasa, S42SelectProyeccionPorAnioyTasa, S42SelectTasa

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


        recaudacion = BuscarRecaudacionSATP(anio, mes, tasas)

        return Response(data={
            "message": "Recaudación obtenida correctamente",
            "content": recaudacion
        }, status=status.HTTP_200_OK)


class S42SelectRecaudacionPorAnioyDependenciaController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        anio = request.query_params.get('anio')
        dependencia = request.query_params.get('dependencia')

        if not anio or not dependencia:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        recaudacion = S42SelectRecaudacionPorAnioyDependencia(anio, dependencia)

        return Response(data={
            "message": "Recaudación obtenida correctamente",
            "content": recaudacion
        }, status=status.HTTP_200_OK)

class S42SelectProyeccionPorAnioyDependenciaController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        opcion = request.query_params.get('opcion')
        anio = request.query_params.get('anio')
        dependencia = request.query_params.get('dependencia')

        if not opcion or not anio or not dependencia:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)


        proyeccion = S42SelectProyeccionPorAnioyDependencia(opcion, anio, dependencia)

        
        return Response(data={
            "message": "Proyección obtenida correctamente",
            "content": proyeccion
        }, status=status.HTTP_200_OK)


class S42SelectRecaudacionPorAnioyTasaController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        anio = request.query_params.get('anio')
        tasa = request.query_params.get('tasa')

        if not anio or not tasa:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        recaudacion = S42SelectRecaudacionPorAnioyTasa(anio, tasa)

        return Response(data={
            "message": "Recaudación obtenida correctamente",
            "content": recaudacion
        }, status=status.HTTP_200_OK)


class S42SelectProyeccionPorAnioyTasaController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        opcion = request.query_params.get('opcion')
        anio = request.query_params.get('anio')
        tasa = request.query_params.get('tasa')

        if not opcion or not anio or not tasa:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        proyeccion = S42SelectProyeccionPorAnioyTasa(opcion, anio, tasa)

        return Response(data={
            "message": "Proyección obtenida correctamente",
            "content": proyeccion   
        }, status=status.HTTP_200_OK)


class S42SelectTasaController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        opcion = request.query_params.get('opcion')
        valor = request.query_params.get('valor')
        if not opcion or not valor:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        tasa = S42SelectTasa(opcion, valor)

        return Response(data={
            "message": "Tasa obtenida correctamente",
            "content": tasa
        }, status=status.HTTP_200_OK)