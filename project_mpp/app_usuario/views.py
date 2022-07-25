from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .serializers import MenuesSerializer, UserMenuesSerializer
from app_usuario.usuario import leerMenues, leerUserMenues

# Create your views here.

class MenuesController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuesSerializer
        
    def get(self, request: Request):

        usuario = request.query_params.get('usuario')
        sistema = request.query_params.get('sistema')
        opcion = request.query_params.get('opcion')
       
        data = self.serializer_class(instance= leerMenues(usuario, sistema, opcion), many=True)

        return Response(data = {
            "message":None,
            "content":data.data
        })

class UserMenuesController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMenuesSerializer
        
    def get(self, request: Request):

        usuario = request.query_params.get('usuario')
        sistema = request.query_params.get('sistema')
        menu_buscado= request.query_params.get('menu')

        select_user_menues = []
        user_menues = leerUserMenues(usuario, sistema)

        if menu_buscado:
            for item_menu in user_menues:
                if item_menu["MenCodi"].startswith(menu_buscado): 
                    select_user_menues.append(item_menu)
        else:
            select_user_menues = user_menues
       
        data = self.serializer_class(instance= select_user_menues, many=True)

        return Response(data = {
            "message":None,
            "content":data.data
        })        


