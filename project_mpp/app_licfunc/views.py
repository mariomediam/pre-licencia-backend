from django.shortcuts import render
from django.db import transaction
from django.db.models import F, Q, ImageField
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .models import PrecalificacionModel, EvalUsuModel, PrecalGiroNegModel, PrecalCuestionarioModel, PrecalEvaluacionModel, PrecalDocumentacionModel, SectoresLicModel, TipoEvalModel, PrecalTipoDocumModel, TipoLicenciaModel, PrecalFirmaArchivoModel
from .serializers import PrecalificacionSerializer, EvalUsuSerializer, PrecalifUserEstadoSerializer, PrecalifContribSerializer, PrecalifGiroNegSerializer, PrecalifCuestionarioSerializer, PrecalEvaluacionSerializer, PrecalEvaluacionTipoSerializer, PrecalDocumentacionSerializer, ListDocumentacionSerializer, TipoEvalSerializer, PrecalTipoDocumSerializer, UploadFileSerializer, TipoLicenciaSerializer, SectoresLicSerializer, PrecalRequisitoArchivoModel
from app_licfunc.licfunc import TipoTramitePorLicencia, BuscarRequisitoArchivo, BuscarLicencGen
from app_deploy.general.enviarEmail import enviarEmail
from app_deploy.general.descargar import download_file
from app_deploy.general.cargar import upload_file

from django.http import FileResponse
import os
from os import environ
from dotenv import load_dotenv
from django.core.files import File
from django.http import HttpResponse

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)


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
        data.data["q_tasa"] = 150.20

        return Response(data={
            "message":"hollaaaa",
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
        tipo_licencia = request.data.get("tipoLicencia")

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
                    precalificacion = PrecalificacionModel.objects.get(pk=precalificacion_id)
                    tipo_eval = data.data["tipoEval"]                    

                    if tipo_eval == 1:                        
                        if precalificacion.precalRiesgoEval != 0:
                            raise Exception("El nivel de riesgo ya ha sido evaluado")
                        if not precal_riesgo:
                            raise Exception("El campo precalRiesgo es requerido")
                                                 
                        precalificacion.precalRiesgoEval = result_eval

                        if result_eval == 1:
                            precalificacion.precalRiesgo = precal_riesgo                        
                        else:
                            precalificacion.precalRiesgo = 0


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

                    if result_eval == 2: 

                        mi_tipo_eval = TipoEvalModel.objects.get(pk=tipo_eval)
                        
                        subject = 'MPP - Observaciones en Solicitud Virtual de Pre Licencia N° ' + f'{precalificacion.precalId:04}'
                        
                        context = {'precalId': f'{precalificacion.precalId:04}', 'nombre_completo': precalificacion.precalSolicitante.webContribNomCompleto, 'tipo_evaluacion' : mi_tipo_eval.tipoEvalNombre, 'eval_comentario': data.data["precalEvalComent"], 'email_usuario': precalificacion.precalCorreo}

                        body =  render_to_string("preLicenciaRechazado.html", context = context)
                        
                        to = [precalificacion.precalCorreo]
                        attachments = []
                        # attachments.append(str(settings.MEDIA_ROOT) +'/app_licfunc/0001.pdf')
                        # attachments.append(str(settings.MEDIA_ROOT) +'/app_licfunc/0002.pdf')

                        print(enviarEmail(subject=subject, body=body, to=to, attachments=attachments))

                    elif result_eval == 1 and tipo_eval == 3:

                        # precalificacion__tipoLicencia = tipo_licencia

                        precalificacion.tipoLicencia_id = tipo_licencia

                        tipo_tramite = TipoTramitePorLicencia('01', '0{}'.format(tipo_licencia),  precalificacion.precalRiesgo, precalificacion.precalArea)

                        precalificacion.tipoTramiteId = tipo_tramite['C_TipTra']
                        precalificacion.tipoTramiteOrigen = tipo_tramite['F_TipTra_Origen']
                        precalificacion.tipoTramiteAnio = tipo_tramite['C_TipTra_Anio']


                        tipos_evaluaciones = TipoEvalModel.objects.all()

                        evaluaciones = PrecalEvaluacionModel.objects.filter(precalificacion_id=precalificacion_id).order_by("precalEvalDigitPC")

                        html_evaluaciones = []

                        for evaluacion in evaluaciones:

                            tipo_eval_nombre = ""
                            for tipo_evaluacion in tipos_evaluaciones:                                
                                if tipo_evaluacion.tipoEvalId == evaluacion.tipoEval_id:
                                    tipo_eval_nombre = tipo_evaluacion.tipoEvalNombre
                                
                            if evaluacion.tipoEval_id == 2:
                                resultado_evaluacion = 'Compatible'
                            else:
                                resultado_evaluacion = 'Aceptado'
                            
                            observaciones_evaluacion = evaluacion.precalEvalComent                            

                            html_evaluaciones.append({'tipo_eval_id':evaluacion.tipoEval_id, 
                                'tipo_eval_nombre': tipo_eval_nombre, 'resultado_evaluacion': resultado_evaluacion, 'observaciones_evaluacion' : observaciones_evaluacion })

                        array_documentos = []
                        if request_documentos:
                            mis_documentos_selecc = PrecalDocumentacionModel.objects.select_related('tipoDocum').filter(evaluacion_id = precalEvalId).values('tipoDocum_id', precalTipDocNombre=F('tipoDocum__precalTipDocNombre'))
                            for documento_selecc in mis_documentos_selecc:
                               array_documentos.append(documento_selecc['precalTipDocNombre'])
                                



                        subject = 'MPP - Solicitud Virtual de Pre Licencia N° ' + f'{precalificacion.precalId:04}'

                        # print(html_evaluaciones)
                        
                        context = {'precalId': f'{precalificacion.precalId:04}', 'nombre_completo': precalificacion.precalSolicitante.webContribNomCompleto, 'html_evaluaciones' : html_evaluaciones, 'eval_comentario': data.data["precalEvalComent"], 'email_usuario': precalificacion.precalCorreo, 'documentos': array_documentos}

                        body =  render_to_string("preLicenciaAceptado.html", context = context)
                        
                        to = [precalificacion.precalCorreo]

                        # print(precalificacion.precalCorreo)
                        
                        enviarEmail(subject=subject, body=body, to=to)

                    

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


class SubirImagenController(CreateAPIView):
    serializer_class = UploadFileSerializer

    def post(self, request: Request):
        print(request.FILES)
        data = self.serializer_class(data=request.FILES)
        print("aaaaaaaaaaaa")
        print(request.data)
        print("bbbbbbbbbbbb")
        print(request.data["idRequisitoArchivo"])
        print("cccccccccccc")

        if data.is_valid():
            archivo = data.save()
            url = request.META.get('HTTP_HOST')

            return Response(data={
                'message': 'Archivo subido exitosamente',
                'content': url + archivo
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message': 'Error al crear el archivo',
                'content': data.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class TipoLicenciaController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TipoLicenciaSerializer
    queryset = TipoLicenciaModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data = {
            "message":None,
            "content":data.data
        })            

class SectoresLicController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectoresLicSerializer
    queryset = SectoresLicModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data = {
            "message":None,
            "content":data.data
        })                    

class SectoresBuscarController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectoresLicSerializer
        
    def get(self, request: Request):
        sector_str = request.query_params.get('sector')
        
        if sector_str is None:
            return Response(data = {
            "message":None,
            "content":[]
        }) 

        sectores =  SectoresLicModel.objects.filter(sectorLicId__in=sector_str.split(","))
        data = self.serializer_class(instance= sectores, many=True)

        return Response(data = {
            "message":None,
            "content":data.data
        })       

class SectoresPorPrecalificacionController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectoresLicSerializer
        
    def get(self, request: Request):

        precal_id = request.query_params.get('precalid')
        
        
        if precal_id is None:
            return Response(data = {
            "message":None,
            "content":[]
        }) 

        sectores =  SectoresLicModel.objects.all()
        data = self.serializer_class(instance= sectores, many=True)

        return Response(data = {
            "message":None,
            "content":data.data
        }) 


class TipoLicenciaPorIdController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TipoLicenciaSerializer
    queryset = TipoLicenciaModel.objects.all()

    def get(self, request, tipoLicenciaId):

        tipo_licencia = self.get_queryset().filter(tipoLicId=tipoLicenciaId).first()       

        data = self.serializer_class(instance=tipo_licencia)

        return Response(data={
            "message":None,
            "content": data.data
        })   



class BuscarRequisitoArchivoController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        opcion = request.query_params.get('opcion')
        valor01 = request.query_params.get('valor01')

        if opcion and valor01:            
            requisito_archivo = BuscarRequisitoArchivo(opcion, valor01)
            return Response({'data': requisito_archivo}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar campo a buscar y valor buscado"
                }, status=status.HTTP_404_NOT_FOUND)


# def prelicenciaDownloadFile(request, filename=''):
#     return download_file(request, filename)

def prelicenciaDownloadFile(request, id=''):
    requisito_archivo = PrecalRequisitoArchivoModel.objects.get(pk=id)
    ruta_file = '{}/{}.pdf'.format(requisito_archivo.precalificacion_id, requisito_archivo.precalRequisito)    
    return download_file(request, ruta_file)    
    

def prelicenciaPreviewFile(request, id=''):
    requisito_archivo = PrecalRequisitoArchivoModel.objects.get(pk=id)
    ruta_file = environ.get('RUTA_REQUISITOS_LICENCIA')  + '{}/{}.pdf'.format(requisito_archivo.precalificacion_id, requisito_archivo.precalRequisito)    
    return FileResponse(open(ruta_file, 'rb'), content_type='application/pdf')


def prelicenciaPreviewFirmaFile(request, id=''):    
    firma_archivo = PrecalFirmaArchivoModel.objects.get(pk=id)
    requisito_archivo = PrecalRequisitoArchivoModel.objects.get(pk=firma_archivo.requisitoArchivo_id)
    ruta_file = environ.get('RUTA_REQUISITOS_LICENCIA')  + '{}/{}'.format(requisito_archivo.precalificacion_id, firma_archivo.precalFirmaNombre)    
    return FileResponse(open(ruta_file, 'rb'), content_type='application/pdf')


class agregarPreLicenciaFirma(CreateAPIView):
    serializer_class = UploadFileSerializer
    queryset = PrecalFirmaArchivoModel.objects.all()


    def post(self, request: Request, id=''):
        
        # Obteniendo ruta y nombre del archivo a grabar 
        precal_requisito_archivo = PrecalRequisitoArchivoModel.objects.all().filter(precalArchivoId=id).first()

        precal_firma_archivo = PrecalFirmaArchivoModel()
        tipo_licencia = self.get_queryset().filter(requisitoArchivo_id=id).aggregate(Max('precalFirmaOrd'))
        
        precal_firma_ord = 1
        if tipo_licencia['precalFirmaOrd__max']:
            precal_firma_ord = tipo_licencia['precalFirmaOrd__max'] + 1
        
        file_name = "{}-f{}.pdf".format(precal_requisito_archivo.precalRequisito, f'{precal_firma_ord:0>3}')
        location = '{}{}/'.format(environ.get('RUTA_REQUISITOS_LICENCIA'), precal_requisito_archivo.precalificacion_id)

        # Grabando archivo
        dataArchivo= request.FILES.copy()
        dataArchivo["location"] = location
        dataArchivo["file_name"] = file_name
        data = self.serializer_class(data=dataArchivo)

        if data.is_valid():
            archivo = data.save()

            # Grabando registro en tabla
            precal_firma_archivo.requisitoArchivo_id = id
            precal_firma_archivo.precalFirmaOrd = precal_firma_ord
            precal_firma_archivo.precalFirmaNombre = file_name
            precal_firma_archivo.precalFirmaRuta = "\\\\192.168.100.20\\archivos2\\solicitudLicenciaTemp\\{}\\{}".format(precal_requisito_archivo.precalificacion_id, file_name)
            precal_firma_archivo.precalFirmaLogin = "Login"
            precal_firma_archivo.precalFirmaEstado = "1"

            precal_firma_archivo.save()

            return Response(data={
                    'message': 'Archivo subido exitosamente',
                    'content': archivo
                }, status=status.HTTP_201_CREATED)

        else:
            return Response(data={
                'message': 'Error al crear el archivo',
                'content': data.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class EliminarPreLicenciaFirma(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id):
        firma_archivo = PrecalFirmaArchivoModel.objects.get(pk=id)
        firma_archivo.precalFirmaEstado = "2"
        firma_archivo.save()

        return Response(data={
                    'message': 'Archivo {} eliminado exitosamente'.format(firma_archivo.precalFirmaNombre),
                    'content': None
                }, status=status.HTTP_201_CREATED)


class VistoBuenoDcPreLicencia(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id):
        precalificacion = PrecalificacionModel.objects.get(pk=id)
        precalificacion.precalDcVbEval = request.data.get("precalDcVbEval")
        precalificacion.precalDcVbObs = request.data.get("precalDcVbObs")
        precalificacion.save()        

        return Response(data={
                    'message': 'Visto bueno de Precalificación grabado con éxito'.format(precalificacion.precalDcVbEval),
                    'content': None
                }, status=status.HTTP_201_CREATED)


class VistoBuenoDlPreLicencia(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id):
        
        licencia_generada = BuscarLicencGen(request.data.get("precalSoliciSimulacion"))        
        licencia_generada[0]["Q_LicGen_TasCal"]

        
        precalificacion = PrecalificacionModel.objects.get(pk=id)


        precalificacion.precalDlVbEval = request.data.get("precalDlVbEval")
        precalificacion.precalSoliciSimulacion = request.data.get("precalSoliciSimulacion")
        precalificacion.precalDlVbObs = request.data.get("precalDlVbObs")
        precalificacion.precalMonto = licencia_generada[0]["Q_LicGen_TasCal"]
        precalificacion.save()        

        return Response(data={
                    'message': 'Visto bueno de Precalificación grabado con éxito'.format(precalificacion.precalDlVbEval),
                    'content': None
                }, status=status.HTTP_201_CREATED)

