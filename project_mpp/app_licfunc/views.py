from django.shortcuts import render
from django.db import transaction
from django.db.models import F, Q
from django.conf import settings
from django.template.loader import get_template
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .models import PrecalificacionModel, EvalUsuModel, PrecalGiroNegModel, PrecalCuestionarioModel, PrecalEvaluacionModel, PrecalDocumentacionModel, TipoEvalModel, PrecalTipoDocumModel
from .serializers import PrecalificacionSerializer, EvalUsuSerializer, PrecalifUserEstadoSerializer, PrecalifContribSerializer, PrecalifGiroNegSerializer, PrecalifCuestionarioSerializer, PrecalEvaluacionSerializer, PrecalEvaluacionTipoSerializer, PrecalDocumentacionSerializer, ListDocumentacionSerializer, TipoEvalSerializer, PrecalTipoDocumSerializer
from app_deploy.general.enviarEmail import enviarEmail



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


class PrecalEvaluacionController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalEvaluacionSerializer
    queryset = PrecalEvaluacionModel.objects.all()

    def get(self, request, precalId):
        precalif_eval = self.get_queryset().filter(precalificacion=precalId)
        data = self.serializer_class(instance=precalif_eval, many=True)

        return Response(data={
            "message":None,
            "content": data.data
        })   

    def post(self, request: Request, precalId):
        data = self.serializer_class(data=request.data)
        result_eval = request.data.get("resultEval")
        precal_riesgo = request.data.get("precalRiesgo")
        request_documentos = request.data.get("documentos")

        if data.is_valid():

            try:
                if not result_eval:
                    raise Exception("El campo resultEval es requerido")

                with transaction.atomic():                    
            
                    data.save()
                    precalEvalId = data.data["precalEvalId"]

                    if request_documentos:                                          
                        data_documentos = ListDocumentacionSerializer(data=request.data)  
                        
                        if not data_documentos.is_valid(): 
                            raise Exception("Documentos invalidos")
                        else:
                            documentos = data_documentos.validated_data.get("documentos")
                            list_documento_model = []
                            for documento in documentos:                
                                
                                documento_model = PrecalDocumentacionModel(evaluacion_id=precalEvalId, tipoDocum_id=documento.get("precalTipDocId"))

                                list_documento_model.append(documento_model)

                            PrecalDocumentacionModel.objects.bulk_create(list_documento_model)
                            
                    precalificacion_id = data.data["precalificacion"]
                    tipo_eval = data.data["tipoEval"]

                    precalificacion = PrecalificacionModel.objects.get(pk=precalificacion_id)
                    if tipo_eval == 1:                        
                        if precalificacion.precalRiesgoEval != 0:
                            raise Exception("El nivel de riesgo ya ha sido evaluado")
                        if not precal_riesgo:
                            raise Exception("El campo precalRiesgo es requerido")
                                                 
                        precalificacion.precalRiesgoEval = result_eval
                        precalificacion.precalRiesgo = precal_riesgo

                        if result_eval == 2: 
                            print("aaaaaaaaa")                           
                            subject = 'MPP - Observaciones en solicitud de licencia de funcionamiento N° ' + f'{precalificacion.precalId:04}'
                            body = data.validated_data.get("precalEvalComent")
                            # print(get_template("templates/preLicenciaRechazado.html"))
                            body =  get_template("templates/preLicenciaRechazado.html")
                            to = ['mmedina@munipiura.gob.pe']   
                            attachments = []
                            attachments.append(str(settings.MEDIA_ROOT) +'/app_licfunc/0001.pdf')
                            attachments.append(str(settings.MEDIA_ROOT) +'/app_licfunc/0002.pdf')

                            print(enviarEmail(subject=subject, body=body, to=to, attachments=attachments))


                    elif tipo_eval == 2:
                        if precalificacion.precalCompatCU != 0:
                            raise Exception("La compatibilidad ya ha sido evaluada")
                        if precalificacion.precalRiesgoEval != 1:
                            raise Exception("El resultado de la evaluación del nivel de riesgo debe ser aprobado")

                        precalificacion.precalCompatCU = result_eval

                    elif tipo_eval == 3:
                        if precalificacion.precalCompatDL != 0:
                            raise Exception("Ya existe evaluación previa")
                        if precalificacion.precalCompatCU != 1:
                            raise Exception("El resultado de la evaluación de Control Urbano debe ser compatible")

                        precalificacion.precalCompatDL = result_eval

                    else:
                        raise Exception("resultEval no reconocido")

                    precalificacion.save()

                    return Response(data={
                        'content': data.data,
                        'message': 'Evaluacion creada exitosamente'
                    })

            except Exception as e:
                return Response(data={
                    'message': e.args,
                    'content': None
                }, status=400)
        else:
            return Response(data={
                'message': 'Error creando evaluacion',
                'content': data.errors
            }, status=400)     


class PrecalEvaluacionTipoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalEvaluacionTipoSerializer
    queryset = PrecalEvaluacionModel.objects.all()

    def get(self, request, precalId, tipoEvalId):
        precalif_eval = self.get_queryset().select_related('precalificacion').filter(precalificacion=precalId).filter(tipoEval = tipoEvalId).first()

        if precalif_eval:
            data = self.serializer_class(instance=precalif_eval)

            return Response(data={
                "message":None,
                "content": data.data
            })
        else:
            return Response(data={
                "message":None,
                "content": None
            })

class PrecalDocumentacionController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalDocumentacionSerializer
    queryset = PrecalDocumentacionModel.objects.all()

    def get(self, request, precalId, tipoEvalId):
        documentacion = self.get_queryset().select_related('evaluacion').select_related('tipoDocum').filter(evaluacion__precalificacion=precalId).filter(evaluacion__tipoEval=tipoEvalId)

        data = self.serializer_class(instance=documentacion, many=True)

        return Response(data={
            "message":None,
            "content": data.data
        })        

    def post(self, request: Request, precalId, tipoEvalId):
        
        data = ListDocumentacionSerializer(data=request.data)        
        print(data)

        if data.is_valid():
            evaluacion = PrecalEvaluacionModel.objects.filter(precalificacion_id=precalId).filter(tipoEval_id=tipoEvalId).first()
            
            documentos = data.validated_data.get("documentos")
            list_documento_model = []
            for documento in documentos:                
                
                documento_model = PrecalDocumentacionModel(evaluacion_id=evaluacion.precalEvalId, tipoDocum_id=documento.get("tipoDocum"))

                list_documento_model.append(documento_model)

            data2 = PrecalDocumentacionModel.objects.bulk_create(list_documento_model)
            print(data2)

            return Response(data={
                "message":None,
                "content": "Registros creados con exito"
            })  

        else:
            return Response(data={
                'message': 'Error grabando documentos',
                'content': data.errors
            }, status=400)


class TipoEvalController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TipoEvalSerializer
    queryset = TipoEvalModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data = {
            "message":None,
            "content":data.data
        })

class PrecalTipoDocumController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalTipoDocumSerializer
    queryset = PrecalTipoDocumModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data = {
            "message":None,
            "content":data.data
        })