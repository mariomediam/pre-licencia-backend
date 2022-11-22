from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from app_contribuyente.contribuyente import BuscarContribNombre, BuscarContribCodigo, ConsultaContribCodigo, ConsultaDocumentoNumero, ListarTipoContribuyente, ConsultaTipoLugar, ConsultaSectores, ConsultaLugaresGeneral, ConsultaTipLugCodigo

# Create your views here.

class BuscarContribNombreController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        nombre_contrib = request.query_params.get('nombre')        

        if nombre_contrib:            
            contribuyente = BuscarContribNombre(nombre_contrib)
            return Response({'data': contribuyente}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar nombre a buscar"
                }, status=status.HTTP_404_NOT_FOUND)


class BuscarContribCodigoController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo_contrib = request.query_params.get('codigo')        

        if codigo_contrib:            
            contribuyente = BuscarContribCodigo(codigo_contrib)
            return Response({'data': contribuyente}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)


class ConsultaContribCodigoController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo_contrib = request.query_params.get('codigo')        

        if codigo_contrib:            
            contribuyente = ConsultaContribCodigo(codigo_contrib)
            return Response({'data': contribuyente}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                


class ConsultaDocumentoNumeroController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):    
        numero_documento = request.query_params.get('numero')        
        if numero_documento:            
            documento = ConsultaDocumentoNumero(numero_documento)

            return Response({'data': documento}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                


class ListarTipoContribuyenteController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        documento = ListarTipoContribuyente()
        return Response({'data': documento}, status=status.HTTP_200_OK)


class ConsultaTipoLugarController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        tipo_lugar = ConsultaTipoLugar()
        return Response({'data': tipo_lugar}, status=status.HTTP_200_OK)


class ConsultaSectoresController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        sectores = ConsultaSectores()
        return Response({'data': sectores}, status=status.HTTP_200_OK)


class ConsultaLugarGeneralController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):    
        codigo = request.query_params.get('codigo', '')
        nombre = request.query_params.get('nombre', '')
        tipo_lugar = request.query_params.get('tiplug', '')
        sector = request.query_params.get('sector', '')
        calificacion = request.query_params.get('calif', '')
        dpto = request.query_params.get('dpto', '')
        prov = request.query_params.get('prov', '')
        dist = request.query_params.get('dist', '')

        lugar = ConsultaLugaresGeneral(codigo, nombre, tipo_lugar, sector, calificacion, dpto, prov, dist)

        return Response({'data': lugar}, status=status.HTTP_200_OK)
        

class ConsultaTipLugController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo = request.query_params.get('codigo')        

        if codigo:            
            tipo_lugar = ConsultaTipLugCodigo(codigo)
            return Response({'data': tipo_lugar}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)   