from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

import xml.etree.ElementTree as ET


from app_indicadores.indicadores import BuscarRecaudacionSATP, S42SelectRecaudacionPorAnioyDependencia, S42SelectProyeccionPorAnioyDependencia, S42SelectRecaudacionPorAnioyTasa, S42SelectProyeccionPorAnioyTasa, S42SelectTasa, S42UpdateTasa, S42InsertarProyecciones, BuscarRecaudacionActasControlSATP, S42SelectCapacitacionTema, S42SelectCapacitacionModalidad, S42SelectCapacitacionCapacitador

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

        if not opcion or valor is None:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        tasa = S42SelectTasa(opcion, valor)

        return Response(data={
            "message": "Tasa obtenida correctamente",
            "content": tasa
        }, status=status.HTTP_200_OK)

class S42UpdateTasaController(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request: Request, tasa: int):
        usuario = request.user.username
        dependencia = request.data.get('dependencia')

        if not dependencia:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        S42UpdateTasa(tasa, dependencia, usuario)

        return Response(data={
            "message": "Tasa actualizada correctamente",
            "content": None
        }, status=status.HTTP_200_OK)


class S42InsertarProyeccionesController(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, tasa: int, anio: int):

        usuario = request.user.username
        proyecciones = request.data.get('proyecciones')

        if not tasa or not anio or not proyecciones:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        
        
        # Construir XML
        root = ET.Element('Proyecciones')
        for item in proyecciones:
            proy = ET.SubElement(root, 'Proyeccion')            
            ET.SubElement(proy, 'M_Mes').text = str(item['M_Mes'])
            ET.SubElement(proy, 'Q_Proyecc_Monto').text = str(item['Q_Proyecc_Monto'])            
        
        xml_proyecciones = ET.tostring(root, encoding='unicode')

        S42InsertarProyecciones(tasa, anio, usuario, xml_proyecciones)

        return Response(data={
            "message": "Proyecciones insertadas correctamente",
            "content": None
        }, status=status.HTTP_200_OK)


class BuscarRecaudacionActasControlSATPController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        anio = request.query_params.get('anio')
        tipo_recaudacion = request.query_params.get('tipo')

        if not anio or not tipo_recaudacion:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)


        recaudacion = BuscarRecaudacionActasControlSATP(anio, tipo_recaudacion)

        return Response(data={
            "message": "Recaudación obtenida correctamente",
            "content": recaudacion
        }, status=status.HTTP_200_OK)


class S42SelectCapacitacionTemaController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        opcion = request.query_params.get('opcion')
        valor = request.query_params.get('valor')

        if not opcion:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        capacitacion = S42SelectCapacitacionTema(opcion, valor)

        return Response(data={
            "message": "Capacitación obtenida correctamente",
            "content": capacitacion
        }, status=status.HTTP_200_OK)

class S42SelectCapacitacionModalidadController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        opcion = request.query_params.get('opcion')
        valor = request.query_params.get('valor')

        if not opcion:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        capacitacion = S42SelectCapacitacionModalidad(opcion, valor)

        return Response(data={
            "message": "Capacitación obtenida correctamente",
            "content": capacitacion
        }, status=status.HTTP_200_OK)

class S42SelectCapacitacionCapacitadorController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request):
        opcion = request.query_params.get('opcion')
        valor = request.query_params.get('valor')

        if not opcion:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)

        capacitacion = S42SelectCapacitacionCapacitador(opcion, valor)

        return Response(data={
            "message": "Capacitación obtenida correctamente",
            "content": capacitacion
        }, status=status.HTTP_200_OK)


