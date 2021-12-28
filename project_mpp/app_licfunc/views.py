from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .models import PrecalificacionModel, EvalUsuModel
from .serializers import PrecalificacionSerializer, EvalUsuSerializer


# Create your views here.

class PrecalificacionController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalificacionSerializer
    queryset = PrecalificacionModel.objects.all()

    # def post(self, request: Request):
    #     data = self.serializer_class(data=request.data)
    #     if data.is_valid():
    #         data.save()
    #         return Response(data={
    #             'content': data.data,
    #             'message': 'Plato creado exitosamente'
    #         })
    #     else:
    #         return Response(data={
    #             'message': 'Error al crear el plato',
    #             'content': data.errors
    #         }, status=400)

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data = {
            "message":None,
            "content":data.data
        })


class EvalUsuController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EvalUsuSerializer
    queryset = EvalUsuModel.objects.all()

    # def get(self, request):
    #     data = self.serializer_class(instance=self.get_queryset(), many=True)
    #     return Response(data = {
    #         "message":None,
    #         "content":data.data
    #     })

    def get(self, request, login):
        evaluacion_usuario = self.get_queryset().filter(userLogin=login)
        data = self.serializer_class(instance=evaluacion_usuario, many=True)

        return Response(data={
            "message":None,
            "content": data.data
        })

class PrecalifUserEstadoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalificacionSerializer
    
    def get(self, request: Request):

        login_buscado = request.query_params.get('login')
        estado_buscado = request.query_params.get('estado')

        tipo_evaluaciones = EvalUsuModel.objects.filter(userLogin=login_buscado)
        precalificaciones = []

        if tipo_evaluaciones:            
            for tipo_eval in tipo_evaluaciones:                
                if tipo_eval.tipoEval.tipoEvalId == 1:
                    precalificacionesTmp = PrecalificacionModel.objects.filter(precalRiesgoEval=estado_buscado).all()
                elif tipo_eval.tipoEval.tipoEvalId == 2:
                    precalificacionesTmp = PrecalificacionModel.objects.filter(precalCompatCU=estado_buscado).filter(precalRiesgoEval=1).all()
                elif tipo_eval.tipoEval.tipoEvalId == 3:
                    precalificacionesTmp = PrecalificacionModel.objects.filter(precalCompatDL=estado_buscado).filter(precalCompatCU=1).all()
                if precalificacionesTmp:
                    precalificaciones.extend(precalificacionesTmp)
                            
        data = self.serializer_class(instance=precalificaciones, many=True)
        return Response(data = {
            "message":None,
            "content":data.data
        })

    