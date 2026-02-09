
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,  RetrieveAPIView
)
from rest_framework.request import Request
from datetime import datetime
from .models import ExpedientesModel
from .serializers import ExpedientesSerializer
from .tradoc import SeleccDocumXNumero, SeleccDocInterno, VerArbol, s17SelectDependencia

# Create your views here.


class ExpedientesController(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ExpedientesModel.objects.all()
    serializer_class = ExpedientesSerializer

    def get(self, request, numero:str = None, anio:str = None):
        if numero is None or anio is None:
            return Response(
                data={"message": "Ingrese número y año de expediente", "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        expediente = ExpedientesModel.objects.filter(ExpedId=numero, ExpedAnio=anio).first() 

        if expediente is None:
            return Response(
                data={"message": None, "content": {}},
                status=status.HTTP_200_OK,
            )
        
        
        data = self.serializer_class(instance=expediente)

        return Response(
            data={"message": None, "content": data.data},
            status=status.HTTP_200_OK,
        )

class SeleccDocumController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        try:

            opcion = request.query_params.get('opcion')
            c_depend = request.query_params.get('c_depend')
            c_docum = request.query_params.get('c_docum')
            m_docum_numdoc = request.query_params.get('m_docum_numdoc')
            desde = request.query_params.get('desde')
            hasta = request.query_params.get('hasta')

           

            if opcion is None:
                return Response(
                    data={"message": "Ingrese opción", "content": None},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if opcion == 'NUMERO':
                if c_depend is None or m_docum_numdoc is None:
                    return Response(
                        data={"message": "Ingrese código de dependencia y número de documento", "content": None},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                data = SeleccDocumXNumero(c_depend, m_docum_numdoc, desde, hasta)

            elif opcion == 'C_DOCUM':
                if c_docum is None:
                    return Response(
                        data={"message": "Ingrese código de documento", "content": None},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                data = SeleccDocInterno(c_docum)

            return Response(
                data={"message": None, "content": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

class VerArbolController(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            c_docum = request.query_params.get('c_docum')
            data = VerArbol(c_docum)
            return Response(
                data={"message": None, "content": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

class VerUltimaRamaArbolController(RetrieveAPIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        try:
            c_docum = request.query_params.get('c_docum')
            arbol = VerArbol(c_docum)
            
            # Si no hay datos, retornar vacío
            if not arbol:
                return Response(
                    data={"message": None, "content": []},
                    status=status.HTTP_200_OK,
                )
            
            # Tomar el último par de C_Docum y C_Docum_Ref
            ultimo_c_docum = arbol[-1]['C_Docum']
            ultimo_c_docum_ref = arbol[-1]['C_Docum_Ref']
            
            # Filtrar todas las filas que coincidan con el último par
            ultima_rama = [
                row for row in arbol 
                if row['C_Docum'] == ultimo_c_docum and row['C_Docum_Ref'] == ultimo_c_docum_ref
            ]
            
            # Ordenar por M_Mapeo_Nivel
            ultima_rama.sort(key=lambda x: x['M_Mapeo_Nivel'])
            
            return Response(
                data={"message": None, "content": ultima_rama},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )



class s17SelectDependenciaController(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        ano = request.query_params.get('ano', datetime.now().year)
        field = request.query_params.get('field')
        valor = request.query_params.get('valor')
        solo_activas = request.query_params.get('solo_activas', 1)
        if not ano or not field or valor is None or not solo_activas:
            return Response(data={
                "message": "Faltan parámetros",
                "content": None
            }, status=status.HTTP_400_BAD_REQUEST)
            
        dependencia = s17SelectDependencia(ano, field, valor, solo_activas)

        print("dependencia", dependencia)
        return Response(data={
            "message": "Dependencia obtenida correctamente",
            "content": dependencia
        }, status=status.HTTP_200_OK)