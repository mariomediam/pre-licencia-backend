import os
from os import environ

from django.shortcuts import render
from django.template.loader import get_template

from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from dotenv import load_dotenv

from app_planif.planif import *

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class SelectPlan_estrategicoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        campo = request.query_params.get('campo')
        valor = request.query_params.get('valor')

        if valor:
            plan_estrategico = SelectPlan_estrategicoController(campo,valor)

            return Response(data={
                    "message":None,
                    "content": plan_estrategico
                }, status=status.HTTP_200_OK)
            # return Response({'data': plan_estrategico}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar valor a buscar"
                }, status=status.HTTP_404_NOT_FOUND)

class InsertPlan_estrategicoController(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:

            n_planest_desc = request.data.get("n_planEst_desc")
            n_user = request.user.username

            InsertPlan_estrategico(n_planest_desc, n_user)

            return Response(data={
                        'message': 'Plan estratégico agregado con éxito',
                        'content': None
                    }, status=status.HTTP_201_CREATED)

        except Exception as e:
                return Response(data={
                    'message': e.args,
                    'content': None
                }, status=400)

class UpdatePlan_estrategicoController(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:

            n_planest_desc = request.data.get("n_planEst_desc")
            c_planest = request.data.get("c_planEst")
            f_planest_activo = request.data.get("f_planEst_activo")
            n_user = request.user.username

            UpdatePlan_estrategico(n_planest_desc, c_planest, f_planest_activo, n_user)

            return Response(data={
                        'message': 'Plan estratégico actualizado con éxito',
                        'content': None
                    }, status=status.HTTP_201_CREATED)

        except Exception as e:
                return Response(data={
                    'message': e.args,
                    'content': None
                }, status=400)

class DeletePlan_estrategicoController(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:

            c_planest = request.data.get("c_planEst")
            f_planest_activo = request.data.get("f_planEst_activo")
            n_user = request.user.username

            DeletePlan_estrategico(c_planest, f_planest_activo, n_user)

            return Response(data={
                        'message': 'Plan estratégico eliminado con éxito',
                        'content': None
                    }, status=status.HTTP_201_CREATED)

        except Exception as e:
                return Response(data={
                    'message': e.args,
                    'content': None
                }, status=400)