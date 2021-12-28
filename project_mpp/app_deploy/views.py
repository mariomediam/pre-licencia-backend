from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import LoginSerializer
from . import trabajador
from app_deploy.seguridad.usuario import login
from rest_framework.permissions import IsAuthenticated


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



        
