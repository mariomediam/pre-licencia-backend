from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .models import PrecalificacionModel, EvalUsuModel, PrecalGiroNegModel, PrecalCuestionarioModel
from .serializers import PrecalificacionSerializer, EvalUsuSerializer, PrecalifUserEstadoSerializer, PrecalifContribSerializer, PrecalifGiroNegSerializer, PrecalifCuestionarioSerializer
from django.db.models import F, Q



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

    def get(self, request, login):
        evaluacion_usuario = self.get_queryset().filter(userLogin=login)
        data = self.serializer_class(instance=evaluacion_usuario, many=True)

        return Response(data={
            "message":None,
            "content": data.data
        })

class PrecalifUserEstadoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifUserEstadoSerializer
        
    def get(self, request: Request):

        login_buscado = request.query_params.get('login')
        estado_buscado = request.query_params.get('estado')

        tipo_evaluaciones = EvalUsuModel.objects.filter(userLogin=login_buscado).values()
        precalificaciones = []
        filtros = []

        if tipo_evaluaciones:            
            for tipo_eval in tipo_evaluaciones:   
                if estado_buscado:
                    if tipo_eval['tipoEval_id'] == 1:
                        filtros.append(Q(precalRiesgoEval=estado_buscado))
                    elif tipo_eval['tipoEval_id'] == 2:
                        filtros.append(Q(precalCompatCU=estado_buscado) & Q(precalRiesgoEval=1))
                    elif tipo_eval['tipoEval_id'] == 3:
                        filtros.append(Q(precalCompatDL=estado_buscado) & Q(precalCompatCU=1))
                else:
                    if tipo_eval['tipoEval_id'] == 1:
                        filtros.append(Q(precalRiesgoEval__isnull=False))
                    elif tipo_eval['tipoEval_id'] == 2:
                        filtros.append(Q(precalRiesgoEval=1))
                    elif tipo_eval['tipoEval_id'] == 3:
                        filtros.append(Q(precalCompatCU=1))


            query = filtros.pop()

            for item in filtros:
                query |= item

            precalificaciones = PrecalificacionModel.objects.select_related('precalSolicitante').values('precalId', 'precalDireccion', 'precalRiesgoEval', 'precalCompatCU', 'precalCompatDL', webContribNomCompleto=F('precalSolicitante__webContribNomCompleto')).filter(query).order_by('precalId')    
                                    
        # data = self.serializer_class(instance= list({v['precalId']:v for v in precalificaciones}.values()), many=True)
        data = self.serializer_class(instance= precalificaciones, many=True)
        return Response(data = {
            "message":None,
            "content":data.data
        })

class PrecalifContribController(RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = PrecalifContribSerializer
    queryset = PrecalificacionModel.objects.all()

    def get(self, request, id):
        precalificaciones = self.get_queryset().get(pk=id)
        data = self.serializer_class(instance=precalificaciones)

        return Response(data={
            "message":None,
            "content": data.data
        })

class PrecalifGiroNegController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifGiroNegSerializer
    queryset = PrecalGiroNegModel.objects.all()

    def get(self, request, precalId):
        precalif_giro_neg = self.get_queryset().select_related('precalificacion').select_related('giroNegocio').filter(precalificacion=precalId)
        data = self.serializer_class(instance=precalif_giro_neg, many=True)

        # precalif_giro_neg = self.get_queryset().filter(precalificacion=precalId)
        # data = self.serializer_class(instance=precalif_giro_neg, many=True)

        return Response(data={
            "message":None,
            "content": data.data
        })

class PrecalifCuestionarioController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifCuestionarioSerializer
    queryset = PrecalCuestionarioModel.objects.all()

    def get(self, request, precalId):
        precalif_cuestionario = self.get_queryset().filter(precalificacion=precalId)
        data = self.serializer_class(instance=precalif_cuestionario, many=True)

        return Response(data={
            "message":None,
            "content": data.data
        })