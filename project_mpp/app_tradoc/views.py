from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,  
)


from .models import ExpedientesModel
from .serializers import ExpedientesSerializer


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