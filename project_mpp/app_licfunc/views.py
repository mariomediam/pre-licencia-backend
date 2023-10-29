import base64
import os
import io
from  PIL import Image
import imghdr
import pdfkit
import mimetypes

from django.shortcuts import render
from django.db import transaction
from django.db.models import F, Q, ImageField, OuterRef, Subquery, Count
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from rest_framework import pagination
from rest_framework.decorators import api_view
from rest_framework import status, mixins
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .models import (
    GiroNegocioModel,
    LicencArchivoModel,
    PrecalificacionModel,
    EvalUsuModel,
    PrecalGiroNegModel,
    PrecalCuestionarioModel,
    PrecalEvaluacionModel,
    PrecalDocumentacionModel,
    SectoresLicModel,
    TipoEvalModel,
    PrecalTipoDocumModel,
    TipoLicenciaModel,
    PrecalFirmaArchivoModel,
    LicencSolModel,
    LicProvTipoModel,
    LicProvUbicaModel,
    LicProvRubroModel,
    LicProvModel,
)
from .serializers import (
    LicencArchivoSerializer,
    PrecalificacionSerializer,
    EvalUsuSerializer,
    PrecalifUserEstadoSerializer,
    PrecalifContribSerializer,
    PrecalifGiroNegSerializer,
    PrecalifCuestionarioSerializer,
    PrecalEvaluacionSerializer,
    PrecalEvaluacionTipoSerializer,
    PrecalDocumentacionSerializer,
    ListDocumentacionSerializer,
    TipoEvalSerializer,
    PrecalTipoDocumSerializer,
    UploadFileSerializer,
    TipoLicenciaSerializer,
    SectoresLicSerializer,
    PrecalRequisitoArchivoModel,
    GiroNegocioSerializer,
    LicencArchivoUploadSerializer,
    LicProvSerializer,
    LicProvTipoSerializer,
    LicProvFullSerializer,
    LicProvRubroSerializer,
    LicProvUbicaSerializer,
    LicProvSerializerImage64
)
from app_licfunc.licfunc import (
    TipoTramitePorLicencia,
    BuscarRequisitoArchivo,
    BuscarLicencGen,
    BuscarDatosTrabajador,
    BuscarTipoTramite,
    ImprimirLicencia,
    BuscarGiroNegocio,
    AgregarSol_GiroNegCiiu,
    SeleccionarSolicitud,
    LicProvisionalBuscar,
    LicProvisionalImprimir,
)
from app_deploy.general.enviarEmail import enviarEmail
from app_deploy.general.descargar import download_file
from app_deploy.general.cargar import upload_file
from app_deploy.general.paginations import CustomPagination
from app_deploy.general.imageToBase64 import imageToBase64
from app_deploy.general.generateQR import generateQrURL
from app_tradoc.tradoc import SeleccReqTupa

from app_contribuyente.models import ContribuyenteModel


from django.http import FileResponse
import os
import shutil
from os import environ
from dotenv import load_dotenv
from django.core.files import File
from django.http import HttpResponse

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

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
        return Response(data={"message": None, "content": data.data})


class EvalUsuController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EvalUsuSerializer
    queryset = EvalUsuModel.objects.all()

    def get(self, request, login):
        evaluacion_usuario = self.get_queryset().filter(userLogin=login)
        data = self.serializer_class(instance=evaluacion_usuario, many=True)

        return Response(data={"message": None, "content": data.data})


class PrecalifUserEstadoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifUserEstadoSerializer

    def get(self, request: Request):
        login_buscado = request.query_params.get("login")
        estado_buscado = request.query_params.get("estado")

        tipo_evaluaciones = EvalUsuModel.objects.filter(
            userLogin=login_buscado
        ).values()
        precalificaciones = []
        filtros = []

        if tipo_evaluaciones:
            for tipo_eval in tipo_evaluaciones:
                if estado_buscado:
                    if tipo_eval["tipoEval_id"] == 1:
                        filtros.append(Q(precalRiesgoEval=estado_buscado))
                    elif tipo_eval["tipoEval_id"] == 2:
                        filtros.append(
                            Q(precalCompatCU=estado_buscado) & Q(precalRiesgoEval=1)
                        )
                    elif tipo_eval["tipoEval_id"] == 3:
                        filtros.append(
                            Q(precalCompatDL=estado_buscado) & Q(precalCompatCU=1)
                        )
                else:
                    if tipo_eval["tipoEval_id"] == 1:
                        filtros.append(Q(precalRiesgoEval__isnull=False))
                    elif tipo_eval["tipoEval_id"] == 2:
                        filtros.append(Q(precalRiesgoEval=1))
                    elif tipo_eval["tipoEval_id"] == 3:
                        filtros.append(Q(precalCompatCU=1))

            query = filtros.pop()

            for item in filtros:
                query |= item

            precalificaciones = (
                PrecalificacionModel.objects.select_related("precalSolicitante")
                .values(
                    "precalId",
                    "precalDireccion",
                    "precalRiesgoEval",
                    "precalCompatCU",
                    "precalCompatDL",
                    "precalDlVbEval",
                    "precalDcVbEval",
                    webContribNomCompleto=F("precalSolicitante__webContribNomCompleto"),
                )
                .filter(query)
                .order_by("precalId")
            )

        # data = self.serializer_class(instance= list({v['precalId']:v for v in precalificaciones}.values()), many=True)
        data = self.serializer_class(instance=precalificaciones, many=True)
        return Response(data={"message": None, "content": data.data})


class PrecalifContribController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifContribSerializer
    queryset = PrecalificacionModel.objects.all()

    def get(self, request, id):
        # precalificaciones = self.get_queryset().get(pk=id)
        precalificaciones = (
            self.get_queryset().filter(precalId=id).filter(precalEstado="1").first()
        )
        data = self.serializer_class(instance=precalificaciones)
        # data.data["q_tasa"] = 150.20

        return Response(data={"message": "", "content": data.data})


class PrecalifGiroNegController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifGiroNegSerializer
    queryset = PrecalGiroNegModel.objects.all()

    def get(self, request, precalId):
        precalif_giro_neg = (
            self.get_queryset()
            .select_related("precalificacion")
            .select_related("giroNegocio")
            .filter(precalificacion=precalId)
        )
        data = self.serializer_class(instance=precalif_giro_neg, many=True)

        # precalif_giro_neg = self.get_queryset().filter(precalificacion=precalId)
        # data = self.serializer_class(instance=precalif_giro_neg, many=True)

        return Response(data={"message": None, "content": data.data})


class PrecalifCuestionarioController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifCuestionarioSerializer
    queryset = PrecalCuestionarioModel.objects.all()

    def get(self, request, precalId):
        precalif_cuestionario = self.get_queryset().filter(precalificacion=precalId)
        data = self.serializer_class(instance=precalif_cuestionario, many=True)

        return Response(data={"message": None, "content": data.data})


class PrecalEvaluacionController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalEvaluacionSerializer
    queryset = PrecalEvaluacionModel.objects.all()

    def get(self, request, precalId):
        precalif_eval = self.get_queryset().filter(precalificacion=precalId)
        data = self.serializer_class(instance=precalif_eval, many=True)

        return Response(data={"message": None, "content": data.data})

    def post(self, request: Request, precalId):
        data = self.serializer_class(data=request.data)
        result_eval = request.data.get("resultEval")
        precal_riesgo = request.data.get("precalRiesgo")
        request_documentos = request.data.get("documentos")
        tipo_licencia = request.data.get("tipoLicencia")
        precal_monto = request.data.get("precalMonto")

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
                            documentos = data_documentos.validated_data.get(
                                "documentos"
                            )
                            list_documento_model = []
                            for documento in documentos:
                                documento_model = PrecalDocumentacionModel(
                                    evaluacion_id=precalEvalId,
                                    tipoDocum_id=documento.get("precalTipDocId"),
                                )

                                list_documento_model.append(documento_model)

                            PrecalDocumentacionModel.objects.bulk_create(
                                list_documento_model
                            )

                    precalificacion_id = data.data["precalificacion"]
                    precalificacion = PrecalificacionModel.objects.get(
                        pk=precalificacion_id
                    )
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
                            raise Exception(
                                "El resultado de la evaluación del nivel de riesgo debe ser aprobado"
                            )

                        precalificacion.precalCompatCU = result_eval

                    elif tipo_eval == 3:
                        if precalificacion.precalCompatDL != 0:
                            raise Exception("Ya existe evaluación previa")
                        if precalificacion.precalCompatCU != 1:
                            raise Exception(
                                "El resultado de la evaluación de Control Urbano debe ser compatible"
                            )

                        precalificacion.precalCompatDL = result_eval

                    else:
                        raise Exception("resultEval no reconocido")

                    if result_eval == 2:
                        mi_tipo_eval = TipoEvalModel.objects.get(pk=tipo_eval)

                        subject = (
                            "MPP - Observaciones en Solicitud Virtual de Pre Licencia N° "
                            + f"{precalificacion.precalId:04}"
                        )

                        context = {
                            "precalId": f"{precalificacion.precalId:04}",
                            "nombre_completo": precalificacion.precalSolicitante.webContribNomCompleto,
                            "tipo_evaluacion": mi_tipo_eval.tipoEvalNombre,
                            "eval_comentario": data.data["precalEvalComent"],
                            "email_usuario": precalificacion.precalCorreo,
                        }

                        body = render_to_string(
                            "preLicenciaRechazado.html", context=context
                        )

                        to = [precalificacion.precalCorreo]
                        attachments = []
                        # attachments.append(str(settings.MEDIA_ROOT) +'/app_licfunc/condicion_minima_seguridad.pdf')
                        # attachments.append(str(settings.MEDIA_ROOT) +'/app_licfunc/0002.pdf')

                        print(
                            enviarEmail(
                                subject=subject,
                                body=body,
                                to=to,
                                attachments=attachments,
                            )
                        )

                    elif result_eval == 1 and tipo_eval == 3:
                        # precalificacion__tipoLicencia = tipo_licencia

                        precalificacion.tipoLicencia_id = tipo_licencia
                        precalificacion.precalMonto = precal_monto

                        tipo_tramite = TipoTramitePorLicencia(
                            "01",
                            "0{}".format(tipo_licencia),
                            precalificacion.precalRiesgo,
                            precalificacion.precalArea,
                        )

                        precalificacion.tipoTramiteId = tipo_tramite["C_TipTra"]
                        precalificacion.tipoTramiteOrigen = tipo_tramite[
                            "F_TipTra_Origen"
                        ]
                        precalificacion.tipoTramiteAnio = tipo_tramite["C_TipTra_Anio"]

                        tipos_evaluaciones = TipoEvalModel.objects.all()

                        evaluaciones = PrecalEvaluacionModel.objects.filter(
                            precalificacion_id=precalificacion_id
                        ).order_by("precalEvalDigitPC")

                        html_evaluaciones = []

                        for evaluacion in evaluaciones:
                            tipo_eval_nombre = ""
                            for tipo_evaluacion in tipos_evaluaciones:
                                if tipo_evaluacion.tipoEvalId == evaluacion.tipoEval_id:
                                    tipo_eval_nombre = tipo_evaluacion.tipoEvalNombre

                            if evaluacion.tipoEval_id == 2:
                                resultado_evaluacion = "Compatible"
                            elif evaluacion.tipoEval_id == 1:
                                if precalificacion.precalRiesgo == 4:
                                    resultado_evaluacion = "RIESGO BAJO"
                                elif precalificacion.precalRiesgo == 5:
                                    resultado_evaluacion = "RIESGO MEDIO"
                                else:
                                    resultado_evaluacion = ""
                            else:
                                resultado_evaluacion = "Aceptado"

                            observaciones_evaluacion = evaluacion.precalEvalComent

                            html_evaluaciones.append(
                                {
                                    "tipo_eval_id": evaluacion.tipoEval_id,
                                    "tipo_eval_nombre": tipo_eval_nombre,
                                    "resultado_evaluacion": resultado_evaluacion,
                                    "observaciones_evaluacion": observaciones_evaluacion,
                                }
                            )

                        array_documentos = []
                        if request_documentos:
                            mis_documentos_selecc = (
                                PrecalDocumentacionModel.objects.select_related(
                                    "tipoDocum"
                                )
                                .filter(evaluacion_id=precalEvalId)
                                .values(
                                    "tipoDocum_id",
                                    precalTipDocNombre=F(
                                        "tipoDocum__precalTipDocNombre"
                                    ),
                                )
                            )
                            for documento_selecc in mis_documentos_selecc:
                                array_documentos.append(
                                    documento_selecc["precalTipDocNombre"]
                                )

                        print("************************ 01 **************************")

                        array_requisitos = []
                        if (
                            precalificacion.tipoTramiteId
                            and precalificacion.tipoTramiteOrigen
                            and precalificacion.tipoTramiteAnio
                        ):
                            requisitos = SeleccReqTupa(
                                precalificacion.tipoTramiteId,
                                precalificacion.tipoTramiteAnio,
                                precalificacion.tipoTramiteOrigen,
                                None,
                                1,
                            )
                            for requito in requisitos:
                                array_requisitos.append(
                                    {
                                        "N_ReqTup_Item": requito["N_ReqTup_Item"],
                                        "N_ReqTup_descrip": requito["N_ReqTup_descrip"],
                                        "N_ReqTup_PdfUrl": requito["N_ReqTup_PdfUrl"],
                                        "N_ReqTup_VidUrl": requito["N_ReqTup_VidUrl"],
                                    }
                                )

                        print("************************ 02 **************************")

                        subject = (
                            "MPP - Solicitud Virtual de Pre Licencia N° "
                            + f"{precalificacion.precalId:04}"
                        )

                        # print(html_evaluaciones)

                        # obj_tipo_licencia = TipoLicenciaModel.objects.all().filter(tipoLicId=tipo_licencia).first()

                        context = {
                            "precalId": f"{precalificacion.precalId:04}",
                            "nombre_completo": precalificacion.precalSolicitante.webContribNomCompleto,
                            "html_evaluaciones": html_evaluaciones,
                            "eval_comentario": data.data["precalEvalComent"],
                            "email_usuario": precalificacion.precalCorreo,
                            "documentos": array_documentos,
                            "tipo_licencia_nombre": precalificacion.tipoLicencia.tipoLicDescrip,
                            "tasa": precalificacion.precalMonto,
                            "requisitos": array_requisitos,
                        }

                        body = render_to_string(
                            "preLicenciaAceptado.html", context=context
                        )

                        to = [precalificacion.precalCorreo]

                        to = ["mmedina@munipiura.gob.pe"]

                        print("************************ 03 **************************")

                        # print(precalificacion.precalCorreo)

                        attachments = []
                        # attachments.append(str(settings.MEDIA_ROOT) +'/app_licfunc/condicion_minima_seguridad.pdf')

                        enviarEmail(
                            subject=subject, body=body, to=to, attachments=attachments
                        )

                        print("************************ 04 **************************")

                    precalificacion.save()

                    if result_eval == 1:
                        EnviarCorreoTerminalista(precalId)

                    return Response(
                        data={
                            "content": data.data,
                            "message": "Evaluacion creada exitosamente",
                        }
                    )

            except Exception as e:
                return Response(data={"message": e.args, "content": None}, status=400)
        else:
            return Response(
                data={"message": "Error creando evaluacion", "content": data.errors},
                status=400,
            )


class PrecalEvaluacionTipoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalEvaluacionTipoSerializer
    queryset = PrecalEvaluacionModel.objects.all()

    def get(self, request, precalId, tipoEvalId):
        precalif_eval = (
            self.get_queryset()
            .select_related("precalificacion")
            .filter(precalificacion=precalId)
            .filter(tipoEval=tipoEvalId)
            .first()
        )

        if precalif_eval:
            data = self.serializer_class(instance=precalif_eval)

            return Response(data={"message": None, "content": data.data})
        else:
            return Response(data={"message": None, "content": None})


class PrecalDocumentacionController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalDocumentacionSerializer
    queryset = PrecalDocumentacionModel.objects.all()

    def get(self, request, precalId, tipoEvalId):
        documentacion = (
            self.get_queryset()
            .select_related("evaluacion")
            .select_related("tipoDocum")
            .filter(evaluacion__precalificacion=precalId)
            .filter(evaluacion__tipoEval=tipoEvalId)
        )

        data = self.serializer_class(instance=documentacion, many=True)

        return Response(data={"message": None, "content": data.data})

    def post(self, request: Request, precalId, tipoEvalId):
        data = ListDocumentacionSerializer(data=request.data)
        # print(data)

        if data.is_valid():
            evaluacion = (
                PrecalEvaluacionModel.objects.filter(precalificacion_id=precalId)
                .filter(tipoEval_id=tipoEvalId)
                .first()
            )

            documentos = data.validated_data.get("documentos")
            list_documento_model = []
            for documento in documentos:
                documento_model = PrecalDocumentacionModel(
                    evaluacion_id=evaluacion.precalEvalId,
                    tipoDocum_id=documento.get("tipoDocum"),
                )

                list_documento_model.append(documento_model)

            data2 = PrecalDocumentacionModel.objects.bulk_create(list_documento_model)
            # print(data2)

            return Response(
                data={"message": None, "content": "Registros creados con exito"}
            )

        else:
            return Response(
                data={"message": "Error grabando documentos", "content": data.errors},
                status=400,
            )


class TipoEvalController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TipoEvalSerializer
    queryset = TipoEvalModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data={"message": None, "content": data.data})


class PrecalTipoDocumController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalTipoDocumSerializer
    queryset = PrecalTipoDocumModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data={"message": None, "content": data.data})


class SubirImagenController(CreateAPIView):
    serializer_class = UploadFileSerializer

    def post(self, request: Request):
        # print(request.FILES)
        data = self.serializer_class(data=request.FILES)
        # print(request.data)
        # print(request.data["idRequisitoArchivo"])
        if data.is_valid():
            archivo = data.save()
            url = request.META.get("HTTP_HOST")

            return Response(
                data={
                    "message": "Archivo subido exitosamente",
                    "content": url + archivo,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                data={"message": "Error al crear el archivo", "content": data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TipoLicenciaController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TipoLicenciaSerializer
    queryset = TipoLicenciaModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data={"message": None, "content": data.data})


class SectoresLicController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectoresLicSerializer
    queryset = SectoresLicModel.objects.all()

    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data={"message": None, "content": data.data})


class SectoresBuscarController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectoresLicSerializer

    def get(self, request: Request):
        sector_str = request.query_params.get("sector")

        if sector_str is None:
            return Response(data={"message": None, "content": []})

        sectores = SectoresLicModel.objects.filter(
            sectorLicId__in=sector_str.split(",")
        )
        data = self.serializer_class(instance=sectores, many=True)

        return Response(data={"message": None, "content": data.data})


class SectoresPorPrecalificacionController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectoresLicSerializer

    def get(self, request: Request):
        precal_id = request.query_params.get("precalid")

        if precal_id is None:
            return Response(data={"message": None, "content": []})

        sectores = SectoresLicModel.objects.all()
        data = self.serializer_class(instance=sectores, many=True)

        return Response(data={"message": None, "content": data.data})


class TipoLicenciaPorIdController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TipoLicenciaSerializer
    queryset = TipoLicenciaModel.objects.all()

    def get(self, request, tipoLicenciaId):
        tipo_licencia = self.get_queryset().filter(tipoLicId=tipoLicenciaId).first()

        data = self.serializer_class(instance=tipo_licencia)

        return Response(data={"message": None, "content": data.data})


class BuscarRequisitoArchivoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        opcion = request.query_params.get("opcion")
        valor01 = request.query_params.get("valor01")

        if opcion and valor01:
            requisito_archivo = BuscarRequisitoArchivo(opcion, valor01)
            return Response({"data": requisito_archivo}, status=status.HTTP_200_OK)

        else:
            return Response(
                data={"message": "Debe de ingresar campo a buscar y valor buscado"},
                status=status.HTTP_404_NOT_FOUND,
            )


# def prelicenciaDownloadFile(request, filename=''):
#     return download_file(request, filename)


def prelicenciaDownloadFile(request, id=""):
    requisito_archivo = PrecalRequisitoArchivoModel.objects.get(pk=id)
    ruta_file = "{}/{}.pdf".format(
        requisito_archivo.precalificacion_id, requisito_archivo.precalRequisito
    )
    return download_file(request, ruta_file)


def prelicenciaPreviewFile(request, id=""):
    requisito_archivo = PrecalRequisitoArchivoModel.objects.get(pk=id)
    precalificacion = PrecalificacionModel.objects.get(
        pk=requisito_archivo.precalificacion_id
    )
    ruta_file = environ.get("RUTA_REQUISITOS_LICENCIA") + "{}/{}.pdf".format(
        requisito_archivo.precalificacion_id, requisito_archivo.precalRequisito
    )
    requisito_archivo = SeleccReqTupa(
        precalificacion.tipoTramiteId,
        precalificacion.tipoTramiteAnio,
        precalificacion.tipoTramiteOrigen,
        requisito_archivo.precalRequisito,
        None,
    )

    if len(requisito_archivo) > 0:
        file_name = "Requisito {}.pdf".format(
            requisito_archivo[0]["N_ReqTup_descrip"][:64]
        )
    else:
        file_name = "Requisito {}_{}.pdf".format(
            requisito_archivo.precalificacion_id, requisito_archivo.precalRequisito
        )

    return FileResponse(
        open(ruta_file, "rb"), content_type="application/pdf", filename=file_name
    )


def prelicenciaPreviewFirmaFile(request, id=""):
    firma_archivo = PrecalFirmaArchivoModel.objects.get(pk=id)
    requisito_archivo = PrecalRequisitoArchivoModel.objects.get(
        pk=firma_archivo.requisitoArchivo_id
    )
    precalificacion = PrecalificacionModel.objects.get(
        pk=requisito_archivo.precalificacion_id
    )

    ruta_file = environ.get("RUTA_REQUISITOS_LICENCIA") + "{}/{}".format(
        requisito_archivo.precalificacion_id, firma_archivo.precalFirmaNombre
    )
    requisito_archivo = SeleccReqTupa(
        precalificacion.tipoTramiteId,
        precalificacion.tipoTramiteAnio,
        precalificacion.tipoTramiteOrigen,
        requisito_archivo.precalRequisito,
        None,
    )

    if len(requisito_archivo) > 0:
        file_name = "Firma {}.pdf".format(requisito_archivo[0]["N_ReqTup_descrip"][:64])
    else:
        file_name = "Firma {}_{}.pdf".format(
            requisito_archivo.precalificacion_id, requisito_archivo.precalRequisito
        )

    return FileResponse(
        open(ruta_file, "rb"), content_type="application/pdf", filename=file_name
    )


class agregarPreLicenciaFirma(CreateAPIView):
    serializer_class = UploadFileSerializer
    queryset = PrecalFirmaArchivoModel.objects.all()

    def post(self, request: Request, id=""):
        # Obteniendo ruta y nombre del archivo a grabar
        precal_requisito_archivo = (
            PrecalRequisitoArchivoModel.objects.all().filter(precalArchivoId=id).first()
        )

        precal_firma_archivo = PrecalFirmaArchivoModel()
        tipo_licencia = (
            self.get_queryset()
            .filter(requisitoArchivo_id=id)
            .aggregate(Max("precalFirmaOrd"))
        )

        precal_firma_ord = 1
        if tipo_licencia["precalFirmaOrd__max"]:
            precal_firma_ord = tipo_licencia["precalFirmaOrd__max"] + 1

        file_name = "{}-f{}.pdf".format(
            precal_requisito_archivo.precalRequisito, f"{precal_firma_ord:0>3}"
        )
        location = "{}{}/".format(
            environ.get("RUTA_REQUISITOS_LICENCIA"),
            precal_requisito_archivo.precalificacion_id,
        )

        # Grabando archivo
        # print("****************** 1 ************************")
        # print("******** request.POST ***********")
        # print(request.POST)
        # print("******** request.content_params ***********")
        # print(request.content_params)
        # print("******** request.headers ***********")
        # print(request.headers)
        # print("******** request.body ***********")
        # print(request.body)
        # print("******** request.META.get('CONTENT_TYPE', '')) ***********")
        # print(request.META.get('CONTENT_TYPE', ''))

        # Parse the header to get the boundary to split the parts.
        # content_type = request.META.get('CONTENT_TYPE', '')
        # print(content_type.encode('ascii'))

        # print("******** request.data ***********")
        # print(request.data)
        # print("******** request.parsers ***********")
        # print(request.parsers)
        # print("******** request.FILES ***********")
        # print(request.FILES)
        dataArchivo = request.FILES.copy()
        # print("****************** 2 ************************")
        dataArchivo["location"] = location
        dataArchivo["file_name"] = file_name
        data = self.serializer_class(data=dataArchivo)

        if data.is_valid():
            archivo = data.save()

            # Grabando registro en tabla
            precal_firma_archivo.requisitoArchivo_id = id
            precal_firma_archivo.precalFirmaOrd = precal_firma_ord
            precal_firma_archivo.precalFirmaNombre = file_name
            precal_firma_archivo.precalFirmaRuta = (
                "\\\\192.168.100.20\\archivos2\\solicitudLicenciaTemp\\{}\\{}".format(
                    precal_requisito_archivo.precalificacion_id, file_name
                )
            )
            precal_firma_archivo.precalFirmaLogin = "Login"
            precal_firma_archivo.precalFirmaEstado = "1"

            precal_firma_archivo.save()

            return Response(
                data={"message": "Archivo subido exitosamente", "content": archivo},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                data={"message": "Error al crear el archivo", "content": data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EliminarPreLicenciaFirma(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id):
        firma_archivo = PrecalFirmaArchivoModel.objects.get(pk=id)
        firma_archivo.precalFirmaEstado = "2"
        firma_archivo.save()

        return Response(
            data={
                "message": "Archivo {} eliminado exitosamente".format(
                    firma_archivo.precalFirmaNombre
                ),
                "content": None,
            },
            status=status.HTTP_201_CREATED,
        )


class VistoBuenoDcPreLicencia(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id):
        precalificacion = PrecalificacionModel.objects.get(pk=id)
        precalificacion.precalDcVbEval = request.data.get("precalDcVbEval")
        precalificacion.precalDcVbObs = request.data.get("precalDcVbObs")
        precalificacion.save()

        EnviarEmailVbPreLicencia(id)

        return Response(
            data={
                "message": "Visto bueno de Precalificación grabado con éxito".format(
                    precalificacion.precalDcVbEval
                ),
                "content": None,
            },
            status=status.HTTP_201_CREATED,
        )


class VistoBuenoDlPreLicencia(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id):
        precalificacion = PrecalificacionModel.objects.get(pk=id)
        precalificacion.precalDlVbEval = request.data.get("precalDlVbEval")
        precalificacion.precalDlVbObs = request.data.get("precalDlVbObs")

        if request.data.get("precalDlVbEval") == 1:
            precalificacion.precalSoliciSimulacion = request.data.get(
                "precalSoliciSimulacion"
            )

        precalificacion.save()

        EnviarEmailVbPreLicencia(id)

        return Response(
            data={
                "message": "Visto bueno de Precalificación grabado con éxito".format(
                    precalificacion.precalDlVbEval
                ),
                "content": None,
            },
            status=status.HTTP_201_CREATED,
        )


def BuscarEmailPorTipEval(tipo_eval_id):
    destinatarios = []
    usuarios_dest = EvalUsuModel.objects.all().filter(tipoEval_id=tipo_eval_id)
    for usuario in usuarios_dest:
        datos_trabajador = BuscarDatosTrabajador(usuario.userLogin)
        if len(datos_trabajador) > 0:
            destinatarios.append(
                {
                    "c_usuari_login": usuario.userLogin.strip(),
                    "n_email": datos_trabajador[0]["n_email"].strip(),
                }
            )

    return destinatarios


def BuscarEmailPorTipEval_toArray(tipo_eval_id):
    destinatarios = BuscarEmailPorTipEval(tipo_eval_id)
    destinatario_array = []
    for destinatario in destinatarios:
        if len(destinatario["n_email"]) > 0:
            destinatario_array.append(destinatario["n_email"])

    # return ",".join(destinatario_array)
    return destinatario_array


def EnviarEmailVbPreLicencia(precal_id):
    precalificacion = (
        PrecalificacionModel.objects.all().filter(precalId=precal_id).first()
    )

    if precalificacion.precalDlVbEval != 0 and precalificacion.precalDcVbEval != 0:
        array_observaciones = []
        if precalificacion.precalDlVbEval == 1 and precalificacion.precalDcVbEval == 1:
            array_observaciones.append(precalificacion.precalDcVbObs)
            array_observaciones.append(precalificacion.precalDlVbObs)

            licencia_generada = BuscarLicencGen(precalificacion.precalSoliciSimulacion)

            tipo_tramite = BuscarTipoTramite(
                precalificacion.tipoTramiteId,
                precalificacion.tipoTramiteAnio,
                precalificacion.tipoTramiteOrigen,
            )

            subject = (
                "MPP - Solicitud Virtual de Pre Licencia N° "
                + f"{precalificacion.precalId:04}"
            )

            tipo_tramite_nombre = ""
            cod_tupa = ""
            if len(tipo_tramite) > 0:
                tipo_tramite_nombre = tipo_tramite[0]["N_TipTra_Nombre"]
                cod_tupa = tipo_tramite[0]["C_Tupa"]

            context = {
                "precalId": f"{precalificacion.precalId:04}",
                "nombre_completo": precalificacion.precalSolicitante.webContribNomCompleto,
                "array_observaciones": array_observaciones,
                "tasa": licencia_generada[0]["Q_LicGen_TasCal"],
                "tipo_tramite_nombre": tipo_tramite_nombre,
                "cod_tupa": cod_tupa,
                "email_usuario": precalificacion.precalCorreo,
            }

            body = render_to_string("preLicenciaVBAceptado.html", context=context)

            to = [precalificacion.precalCorreo]
            # to =['mmedina@munipiura.gob.pe']

            enviarEmail(subject=subject, body=body, to=to)

        else:
            if (
                precalificacion.precalDlVbEval == 2
                or precalificacion.precalDcVbEval == 2
            ):
                array_observaciones = []
                if precalificacion.precalDlVbEval == 2:
                    array_observaciones.append(precalificacion.precalDlVbObs)
                if precalificacion.precalDcVbEval == 2:
                    array_observaciones.append(precalificacion.precalDcVbObs)

                subject = (
                    "MPP - Observaciones en Solicitud Virtual de Pre Licencia N° "
                    + f"{precalificacion.precalId:04}"
                )

                context = {
                    "precalId": f"{precalificacion.precalId:04}",
                    "nombre_completo": precalificacion.precalSolicitante.webContribNomCompleto,
                    "tipo_evaluacion": "Requisitos para ingresar expediente",
                    "array_observaciones": array_observaciones,
                    "email_usuario": precalificacion.precalCorreo,
                }

                body = render_to_string("preLicenciaVBRechazado.html", context=context)

                to = [precalificacion.precalCorreo]
                # to = ['mmedina@munipiura.gob.pe']

                enviarEmail(subject=subject, body=body, to=to)


def EnviarCorreoTerminalista(precalId):
    precalificacion = (
        PrecalificacionModel.objects.all().filter(precalId=precalId).first()
    )

    if precalificacion:
        if (
            precalificacion.precalRiesgoEval == 2
            or precalificacion.precalCompatCU == 2
            or precalificacion.precalCompatDL == 2
            or precalificacion.precalDlVbEval == 2
            or precalificacion.precalDcVbEval == 2
        ):
            return {"message": "La precalificación ha sido rechazada", "content": []}

        destino = "indeterminado"
        destinatarios = ""
        if precalificacion.precalRiesgoEval == 0:
            destinatarios = BuscarEmailPorTipEval_toArray(1)
            destino = "evaluar el Nivel de Riesgo"
        elif precalificacion.precalCompatCU == 0:
            destinatarios = BuscarEmailPorTipEval_toArray(2)
            destino = "evaluar Compatibilidad de Uso"
        elif precalificacion.precalCompatDL == 0:
            destinatarios = BuscarEmailPorTipEval_toArray(3)
            destino = "evaluar requisitos para licencia de funcionamiento"
        else:
            destino = ""
            destinatariosVbNr = []
            destinatariosVnAc = []
            if precalificacion.precalDlVbEval == 0:
                destinatariosVnAc = BuscarEmailPorTipEval_toArray(3)
                destino = "evaluar visto bueno para licencia de funcionamiento"
            if precalificacion.precalDcVbEval == 0:
                destinatariosVbNr = BuscarEmailPorTipEval_toArray(1)
                destino = "evaluar visto bueno para licencia de funcionamiento"
            temp = set(destinatariosVnAc) - set(destinatariosVbNr)
            destinatarios = destinatariosVbNr + list(temp)

        if len(destinatarios) > 0:
            subject = (
                "Evaluación pendiente - Solicitud Virtual de Pre Licencia N° "
                + f"{precalId:04}"
            )
            context = {"precalId": precalId, "evaluacion_pendiente": destino}
            body = render_to_string(
                "preLicenciaAlertaTerminalista.html", context=context
            )
            enviarEmail(subject=subject, body=body, to=destinatarios)

        return {"message": "Correo enviado", "content": [",".join(destinatarios)]}
    else:
        return {"message": "No existe precalificación", "content": []}


class EnviarCorreoTerminalistaController(RetrieveAPIView):
    def post(self, request: Request, precalId):
        precalificacion = (
            PrecalificacionModel.objects.all().filter(precalId=precalId).first()
        )
        id_solicitante = request.data.get("idSolicitante")

        if id_solicitante:
            if int(id_solicitante) == precalificacion.precalSolicitante_id:
                data = EnviarCorreoTerminalista(precalId)
                return Response(data={"message": "1", "content": []})

        return Response(data={"message": None, "content": []})


class PrecalifUserEstadoPaginationController(ListAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = PrecalifUserEstadoSerializer
    pagination_class = CustomPagination
    queryset = PrecalificacionModel.objects.all()

    def get(self, request: Request):
        login_buscado = request.query_params.get("login")
        estado_buscado = request.query_params.get("estado")
        filtro_buscado = request.query_params.get("filtro")

        tipo_evaluaciones = EvalUsuModel.objects.filter(
            userLogin=login_buscado
        ).values()
        precalificaciones = []
        filtros = []

        if tipo_evaluaciones:
            for tipo_eval in tipo_evaluaciones:
                if estado_buscado:
                    if tipo_eval["tipoEval_id"] == 1:
                        filtros.append(
                            Q(precalRiesgoEval=estado_buscado)
                            | Q(
                                Q(farchivos__isnull=False)
                                & Q(precalDcVbEval=estado_buscado)
                            )
                        )
                    elif tipo_eval["tipoEval_id"] == 2:
                        filtros.append(
                            Q(precalCompatCU=estado_buscado) & Q(precalRiesgoEval=1)
                        )
                    elif tipo_eval["tipoEval_id"] == 3:
                        filtros.append(
                            Q(Q(precalCompatDL=estado_buscado) & Q(precalCompatCU=1))
                            | Q(
                                Q(farchivos__isnull=False)
                                & Q(precalDlVbEval=estado_buscado)
                            )
                        )
                else:
                    if tipo_eval["tipoEval_id"] == 1:
                        filtros.append(Q(precalRiesgoEval__isnull=False))
                    elif tipo_eval["tipoEval_id"] == 2:
                        filtros.append(Q(precalRiesgoEval=1))
                    elif tipo_eval["tipoEval_id"] == 3:
                        filtros.append(Q(precalCompatCU=1))

            query = filtros.pop()

            # filtros.append(Q(precalEstado="1"))

            for item in filtros:
                query |= item

        if filtro_buscado:
            if filtro_buscado.isnumeric():
                query &= Q(precalId=filtro_buscado)
            else:
                query &= Q(
                    precalSolicitante__webContribNomCompleto__contains=filtro_buscado
                )

        archivos_query = (
            PrecalRequisitoArchivoModel.objects.values("precalificacion_id")
            .distinct()
            .filter(precalificacion=OuterRef("pk"))
        )

        queryset = (
            PrecalificacionModel.objects.select_related("precalSolicitante")
            .values(
                "precalId",
                "precalDireccion",
                "precalRiesgoEval",
                "precalCompatCU",
                "precalCompatDL",
                "precalDlVbEval",
                "precalDcVbEval",
                webContribNomCompleto=F("precalSolicitante__webContribNomCompleto"),
            )
            .annotate(farchivos=Subquery(archivos_query))
            .filter(precalEstado="1")
            .filter(query)
            .order_by("precalId")
        )

        serializer = self.serializer_class(queryset, many=True)

        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class GiroNegocioPaginationController(ListAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = GiroNegocioSerializer
    pagination_class = CustomPagination
    queryset = GiroNegocioModel.objects.all()

    def get(self, request: Request):
        ciiu_buscado = request.query_params.get("ciiu")
        nombre_buscado = request.query_params.get("nombre")

        queryset = self.get_queryset()
        if ciiu_buscado and nombre_buscado:
            queryset = (
                self.get_queryset()
                .filter(giroNegCIIU__contains=ciiu_buscado)
                .filter(giroNegNombre__contains=nombre_buscado)
            )
        elif ciiu_buscado:
            queryset = self.get_queryset().filter(giroNegCIIU__contains=ciiu_buscado)
        elif nombre_buscado:
            queryset = self.get_queryset().filter(
                giroNegNombre__contains=nombre_buscado
            )

        serializer = self.serializer_class(instance=queryset, many=True)

        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class PrecalificacionPruebaController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        tiptra = request.query_params.get("tiptra")
        tiptra_anio = request.query_params.get("tiptra_anio")
        tiptra_origen = request.query_params.get("tiptra_origen")
        reqtup_item = request.query_params.get("reqtup_item")
        ocultar_recpag = request.query_params.get("ocultar_recpag")

        if tiptra and tiptra_anio and tiptra_origen:
            requisito_archivo = SeleccReqTupa(
                tiptra, tiptra_anio, tiptra_origen, reqtup_item, ocultar_recpag
            )

            return Response(
                data={"message": None, "content": requisito_archivo},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                data={"message": "Debe de ingresar código de trámite"},
                status=status.HTTP_404_NOT_FOUND,
            )


class LicencArchivoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicencArchivoSerializer
    queryset = LicencArchivoModel.objects.all()

    def get(self, request, licenc_file):
        licenc_archivo = self.get_queryset().filter(licencFile=licenc_file)
        data = self.serializer_class(instance=licenc_archivo, many=True)

        return Response(data={"message": None, "content": data.data})


class AgregarLicencArchivoController(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicencArchivoSerializer
    queryset = LicencArchivoModel.objects.all()
    file_serializer_class = UploadFileSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            with transaction.atomic():
                licenc_nro = data.validated_data.get("licencNro")
                licenc_origen = data.validated_data.get("licencOrigen")
                licenc_ord_renov = data.validated_data.get("licencOrdRenov")

                LicencArchivoModel.objects.filter(licencNro=licenc_nro).filter(
                    licencOrigen=licenc_origen
                ).filter(licencOrdRenov=licenc_ord_renov).update(licencEstado="2")

                data.save()

                #  Grabando archivo
                file_name = "{}.pdf".format(data.data["licencFile"])
                location = "{}licenciaFuncionamiento/".format(
                    environ.get("RUTA_REQUISITOS_LICENCIA")
                )

                dataArchivo = request.FILES.copy()
                dataArchivo["location"] = location
                dataArchivo["file_name"] = file_name
                data_archivo_serialized = self.file_serializer_class(data=dataArchivo)

                if data_archivo_serialized.is_valid():
                    data_archivo_serialized.save()
                    licencia_archivo = LicencArchivoModel.objects.get(
                        pk=data.data["licencFile"]
                    )
                    licencia_archivo.licencFileNombre = file_name
                    licencia_archivo.licencFileRuta = "{}{}".format(location, file_name)
                else:
                    raise Exception(data_archivo_serialized.errors)

                # Enviando email
                licenc_sol = (
                    LicencSolModel.objects.all()
                    .filter(licencNro=licenc_nro)
                    .filter(licencOrigen=licenc_origen)
                    .first()
                )

                if licenc_sol:
                    solicitud = licenc_sol.soliciSimulacion

                    precalificacion = (
                        PrecalificacionModel.objects.all()
                        .filter(precalSoliciSimulacion=solicitud)
                        .first()
                    )

                    if precalificacion:
                        licencia_archivo.licencEmail = precalificacion.precalCorreo
                        licencia_archivo.save()

                        licencia_impresa = ImprimirLicencia(licenc_nro, licenc_origen)

                        lic_titular = ""
                        lic_nombre_comercial = ""
                        lic_ubicacion = ""
                        lic_actividad_comercial = ""
                        lic_area = 0.00
                        lic_horario = ""
                        lic_tipo_licencia = ""
                        lic_nivel_riesgo = ""
                        lic_fecha_emision = ""

                        if len(licencia_impresa) > 0:
                            lic_titular = licencia_impresa[0]["NomTitular"]
                            lic_nombre_comercial = licencia_impresa[0][
                                "N_LICENC_RAZONSOCIAL"
                            ]
                            lic_ubicacion = licencia_impresa[0]["T_Domic_Negocio"]
                            lic_actividad_comercial = licencia_impresa[0]["T_Giros"]
                            lic_area = licencia_impresa[0]["Q_LICENC_AREA"]
                            lic_horario = licencia_impresa[0]["T_Horario"]
                            lic_tipo_licencia = licencia_impresa[0]["n_tiplic_nombre"]
                            lic_nivel_riesgo = licencia_impresa[0]["N_NivRie"]
                            lic_fecha_emision = licencia_impresa[0]["T_FecEmi"]

                        subject = (
                            "MPP - Solicitud Virtual de Pre Licencia N° "
                            + f"{precalificacion.precalId:04}"
                        )

                        context = {
                            "precalId": f"{precalificacion.precalId:04}",
                            "licencNro": licenc_nro,
                            "nombre_completo": precalificacion.precalSolicitante.webContribNomCompleto,
                            "email_usuario": precalificacion.precalCorreo,
                            "tipo_licencia_nombre": precalificacion.tipoLicencia.tipoLicDescrip,
                            "lic_titular": lic_titular,
                            "lic_nombre_comercial": lic_nombre_comercial,
                            "lic_ubicacion": lic_ubicacion,
                            "lic_actividad_comercial": lic_actividad_comercial,
                            "lic_area": lic_area,
                            "lic_horario": lic_horario,
                            "lic_tipo_licencia": lic_tipo_licencia,
                            "lic_nivel_riesgo": lic_nivel_riesgo,
                            "lic_fecha_emision": lic_fecha_emision,
                        }

                        body = render_to_string("LicenciaEnviada.html", context=context)

                        to = [precalificacion.precalCorreo]

                        # to = ['mmedina@munipiura.gob.pe']

                        ruta_testino_tmp = "{}/app_licfunc/Licencia_{}.pdf".format(
                            str(settings.MEDIA_ROOT), licenc_nro
                        )

                        shutil.copyfile(
                            "{}/{}".format(location, file_name), ruta_testino_tmp
                        )

                        attachments = []
                        attachments.append(ruta_testino_tmp)

                        enviarEmail(
                            subject=subject, body=body, to=to, attachments=attachments
                        )

                        if os.path.exists(ruta_testino_tmp):
                            os.remove(ruta_testino_tmp)

                return Response(
                    data={
                        "content": LicencArchivoSerializer(licencia_archivo).data,
                        "message": "Licencia enviada exitosamente a {}".format(
                            precalificacion.precalCorreo
                        ),
                    }
                )

        else:
            return Response(
                data={"message": "Error al crear el registro", "content": data.errors},
                status=400,
            )


def licenciaPreviewFile(request, id=""):
    licencia_archivo = LicencArchivoModel.objects.get(pk=id)
    ruta_file = "{}licenciaFuncionamiento/{}.pdf".format(
        environ.get("RUTA_REQUISITOS_LICENCIA"), id
    )
    file_name = "Licencia_{}.pdf".format(licencia_archivo.licencNro)
    return FileResponse(
        open(ruta_file, "rb"), content_type="application/pdf", filename=file_name
    )


def licenciaDownloadFile(request, id=""):
    licencia = LicencArchivoModel.objects.get(pk=id)
    ruta_file = "licenciaFuncionamiento/{}.pdf".format(id)
    return download_file(request, ruta_file, "Licencia_{}".format(licencia.licencNro))


class BuscarGiroNegocioController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        area = request.query_params.get("area")
        xml_giros = request.query_params.get("giros")
        area_mayor30 = request.query_params.get("mayor30")

        if area:
            giros_negocios = BuscarGiroNegocio(area, xml_giros, area_mayor30)

            return Response(
                data={"message": None, "content": giros_negocios},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                data={"message": "Debe de ingresar área del negocio"},
                status=status.HTTP_404_NOT_FOUND,
            )


class AgregarSol_GiroNegCiiuController(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id=""):
        giros_solicitud = request.data.get("giros")
        login = request.data.get("login")

        if id and giros_solicitud and login:
            try:
                with transaction.atomic():
                    for giro in giros_solicitud:
                        AgregarSol_GiroNegCiiu(id, giro, login)

                    return Response(
                        data={
                            "message": "Giros ingresados correctamente",
                            "content": "",
                        },
                        status=status.HTTP_200_OK,
                    )

            except Exception as e:
                return Response(data={"message": e.args, "content": None}, status=400)
        else:
            return Response(
                data={
                    "message": "Debe ingresar solicitud, giros y login",
                    "content": None,
                },
                status=400,
            )


class SeleccionarSolicitudController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        c_solici = request.query_params.get("solicitud")

        if c_solici:
            solicitud = SeleccionarSolicitud(c_solici)

            if len(solicitud) > 0:
                solicitud = solicitud[0]
            else:
                solicitud = {}

            return Response(
                data={"message": None, "content": solicitud}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                data={"message": "Debe de ingresar solicitud"},
                status=status.HTTP_404_NOT_FOUND,
            )


class LicProvTipoController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicProvTipoSerializer
    queryset = LicProvTipoModel.objects.all()

    def get(self, request, id=None):
        if id:
            lic_prov_tipo = self.get_queryset().get(pk=id)
            data = self.serializer_class(instance=lic_prov_tipo, many=False)
        else:
            lic_prov_tipo = self.get_queryset()
            data = self.serializer_class(instance=lic_prov_tipo, many=True)

        
        return Response(data={"message": None, "content": data.data})


class LicProvBuscarController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicProvFullSerializer

    def get(self, request: Request):
        lic_prov_tipo = request.query_params.get("tipo")
        campo_buscado = request.query_params.get("campo")
        valor_buscado = request.query_params.get("valor")        
        
        lic_prov_tipo = int(lic_prov_tipo)

        campos_validos = [
            "todos",
            "autoriza",
            "expediente",
            "rubro",
            "ubica",
            "formato",
            "titular",
        ]

        if campo_buscado not in campos_validos:
            return Response(
                data={"message": "El campo buscado no es válido", "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lic_provisional = LicProvisionalBuscar(
            lic_prov_tipo, campo_buscado, valor_buscado
        )


        # Convirtiendo imagen a base64        
        for i, lic in enumerate(lic_provisional):

            # ruta_imagen = str(lic["N_LicProv_TitImg"]).replace("/var/www/licenciaProvisional/", "Y:\\")
            ruta_imagen = str(lic["N_LicProv_TitImg"])
            
            if os.path.exists(ruta_imagen.strip()):            
                with open(ruta_imagen, "rb") as f:
                    imagen_codificada = base64.b64encode(f.read()).decode("utf-8")
            else:
                imagen_codificada = None
            
            lic_provisional[i]["N_Imagen_Base64"] = imagen_codificada


        lic_provisional_formato = []

        numeros_unicos = {lic["M_LicProv_Nro"] for lic in lic_provisional}

        for numero in numeros_unicos:
            permisos = []
            for lic in lic_provisional:
                if lic["M_LicProv_Nro"] == numero:
                    permisos.append(lic)

            anulada = False
            if len(permisos) > 0:
                anulada = permisos[0]["F_LicProv_Anula"] 
                
            lic_provisional_formato.append(
                {
                    "C_LicProv_Tipo": lic_prov_tipo,
                    "M_LicProv_Nro": numero,
                    "F_LicProv_Anula": anulada,
                    "permisos": permisos,
                }
            )

        return Response(
            data={"message": None, "content": lic_provisional_formato},
            status=status.HTTP_200_OK,
        )


class LicProvCampoBuscarController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        mapea_campos = [
            {
                "display": "Nº autoriza",
                "value": "autoriza",
            },
            {
                "display": "Titular",
                "value": "titular",
            },
            {
                "display": "Rubro",
                "value": "rubro",
            },
            {
                "display": "Ubicación",
                "value": "ubica",
            },
            {
                "display": "Nº expediente",
                "value": "expediente",
            },
            {
                "display": "Nº formato",
                "value": "formato",
            },
            {
                "display": "Listar todos",
                "value": "todos",
            }
        ]

           
        
        return Response(data={"message": None, "content": list(mapea_campos)})


class LicProvRubroController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicProvRubroSerializer
    queryset = LicProvRubroModel.objects.all()

    def get(self, request, id=None):
        if id:
            lic_prov_rubro = self.get_queryset().get(pk=id)
            data = self.serializer_class(instance=lic_prov_rubro, many=False)
        else:
            lic_prov_rubro = self.get_queryset()
            data = self.serializer_class(instance=lic_prov_rubro, many=True)

        
        return Response(data={"message": None, "content": data.data})
    
# class LicProvRubroController(RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = LicProvRubroSerializer
#     queryset = LicProvRubroModel.objects.all()

#     def get(self, request, id=None):
#         if id:
#             lic_prov_rubro = self.get_queryset().get(pk=id)
#             data = self.serializer_class(instance=lic_prov_rubro, many=False)
#         else:
#             lic_prov_rubro = self.get_queryset()
#             data = self.serializer_class(instance=lic_prov_rubro, many=True)

        
#         return Response(data={"message": None, "content": data.data})    
    

class BuscarLicProvRubroController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicProvRubroSerializer
    queryset = LicProvRubroModel.objects.all()

    def get(self, request, tipo:int, orden:int = None):

        lic_prov_rubro = self.get_queryset().filter(licProvTipo=tipo)

        if orden:
            lic_prov_rubro = lic_prov_rubro.filter(rubroOrden=orden).first()
            
            if not lic_prov_rubro:
                return Response(data={"message": None, "content": {}})
            
            data = self.serializer_class(instance=lic_prov_rubro, many=False)   
                        
        else:
            data = self.serializer_class(instance=lic_prov_rubro, many=True)        
        
        return Response(data={"message": None, "content": data.data})        
    

class LicProvUbicaController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicProvUbicaSerializer
    queryset = LicProvUbicaModel.objects.all()

    def get(self, request, id=None):
        if id:
            lic_prov_ubica = self.get_queryset().get(pk=id)
            data = self.serializer_class(instance=lic_prov_ubica, many=False)
        else:
            lic_prov_ubica = self.get_queryset()
            data = self.serializer_class(instance=lic_prov_ubica, many=True)

        
        return Response(data={"message": None, "content": data.data})    


class BuscarLicProvUbicaController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicProvUbicaSerializer
    queryset = LicProvUbicaModel.objects.all()

    def get(self, request, tipo:int, orden:int = None):

        lic_prov_ubica = self.get_queryset().filter(licProvTipo=tipo)

        if orden:
            lic_prov_ubica = lic_prov_ubica.filter(ubicaOrden=orden).first()
            
            if not lic_prov_ubica:
                return Response(data={"message": None, "content": {}})
            
            data = self.serializer_class(instance=lic_prov_ubica, many=False)   
                        
        else:
            data = self.serializer_class(instance=lic_prov_ubica, many=True)        
        
        return Response(data={"message": None, "content": data.data})                

def getLicProvMaxNro(tipo:int):
    lic_prov = LicProvModel.objects.filter(licProvTipo=tipo).aggregate(Max('licProvNro'))
    return  lic_prov["licProvNro__max"] 

def saveImageBase64(image_base64, image_name):
    if image_base64:
        image_data = base64.b64decode(image_base64)
        extension = imghdr.what(None, h=image_data)
        if extension:
            image_name_with_extension = "{}.{}".format(image_name, extension)
        else:
            image_name_with_extension = image_name
        image = Image.open(io.BytesIO(image_data))
        image.save(image_name_with_extension)
        return extension or ""
    else:
        return None
    
def addLicProv(licprov_data, img_titular):
    try:    
        licprov_new = licprov_data.save()        
        path_TitImg = "{}titular-{}".format(environ.get("RUTA_LIVPROV_TITULAR"), licprov_new.licProvId)
        extension = saveImageBase64(img_titular, path_TitImg)
        licprov_new.licProvTitImg =  "{}.{}".format(path_TitImg, extension)
        licprov_new.save()
        return licprov_new
    except Exception as e:
        raise Exception(e)
    
def editLicProv(licprov_data, img_titular):
    try:    
        lic_prov_id = licprov_data.initial_data["licProvId"]
        licprov_edit = LicProvModel.objects.all().get(pk=lic_prov_id)
        licprov_edit.licProvExpNro = licprov_data.validated_data["licProvExpNro"]
        licprov_edit.licProvExpAnio = licprov_data.validated_data["licProvExpAnio"]
        licprov_edit.licProvTitCod = licprov_data.validated_data["licProvTitCod"]
        licprov_edit.licProvTitTipCod = licprov_data.validated_data["licProvTitTipCod"]
        licprov_edit.licProvTitNroDoc = licprov_data.validated_data["licProvTitNroDoc"]        
        licprov_edit.licProvRubro = licprov_data.validated_data["licProvRubro"]
        licprov_edit.licProvUbica = licprov_data.validated_data["licProvUbica"]
        licprov_edit.licProvHorAte = licprov_data.validated_data["licProvHorAte"]
        licprov_edit.licProvCerGas = licprov_data.validated_data["licProvCerGas"]
        licprov_edit.licProvObs = licprov_data.validated_data["licProvObs"]
        licprov_edit.licProvFecEmi = licprov_data.validated_data["licProvFecEmi"]
        licprov_edit.licProvIniVig = licprov_data.validated_data["licProvIniVig"]
        licprov_edit.licProvFinVig = licprov_data.validated_data["licProvFinVig"]
        licprov_edit.licProvFormato = licprov_data.validated_data["licProvFormato"]
        licprov_edit.licProvLogin = licprov_data.validated_data["licProvLogin"]
        licprov_edit.licProvDigitFecha = licprov_data.initial_data["licProvDigitFecha"]
        licprov_edit.licProvDigitPC = licprov_data.validated_data["licProvDigitPC"]

        path_TitImg = "{}titular-{}".format(environ.get("RUTA_LIVPROV_TITULAR"), lic_prov_id)
        extension = saveImageBase64(img_titular, path_TitImg)
        licprov_edit.licProvTitImg = "{}.{}".format(path_TitImg, extension)        

        licprov_edit.save()                
        return licprov_edit

    except Exception as e:
        raise Exception(e)


class LicProvController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LicProvSerializer
    queryset = LicProvModel.objects.all()

    def post(self, request: Request):

        try:
            TIPO_ACCION = { 1:  "nuevo", 2: "modificar", 3: "renovar"}
            login = request.user.username
            data = self.serializer_class(data=request.data) 
                
            accion = data.initial_data["accion"] or 0

            if accion not in TIPO_ACCION:
                return Response(data={"message": "No se ha especificado acción", "content": None}, status=400)
            
            if TIPO_ACCION[accion] == "nuevo":
                licprov_nro_new = getLicProvMaxNro(data.initial_data["licProvTipo"])
                if not licprov_nro_new:
                    licprov_nro_new = 1
                else:
                    licprov_nro_new += 1

                data.initial_data["licProvNro"] = licprov_nro_new
                data.initial_data["licProvRenov"] = None
                            
            img_titular = data.initial_data["licProvTitImg"]
            if len(img_titular) > 0:
                data.initial_data["licProvTitImg"] = "Temporal"

            data.initial_data["licProvLogin"] = login
            data.initial_data["licProvDigitPC"] = request.META.get("REMOTE_ADDR")

            if data.is_valid():
                
                with transaction.atomic():
                    if TIPO_ACCION[accion] == "nuevo":
                        licprov_gestion = addLicProv(data, img_titular)                                                
                    elif TIPO_ACCION[accion] == "modificar":                        
                        licprov_gestion = editLicProv(data, img_titular)

            else:                 
                return Response(
                data={"message": data.errors, "content": "Error creando licencia provisional"},
                status=400,
                )

            return Response(data={"message": None, "content": data.data}, status=200)   
        
        except Exception as e:
                return Response(data={"message": e.args, "content": None}, status=400)


    
    def get(self, request, id):
        try:
            lic_prov = self.get_queryset().get(pk=id)
            data = LicProvSerializerImage64(instance=lic_prov, many=False)
            
            return Response(data={"message": None, "content": data.data}, status=200)
            
        except Exception as e:
            return Response(data={"message": e.args, "content": None}, status=400)
        
def LicProvDownloadController(request, id=""):
           
    lic_provisional = LicProvisionalImprimir(id)

    
    if len(lic_provisional) == 1:
        lic_provisional = lic_provisional[0]        
        image_base_64 = imageToBase64(lic_provisional["N_LicProv_TitImg"])
        url_QR = generateQrURL("https://www.gob.pe/munipiura")
        
        # ********************* INCIO GENERANDO PDF ********************* #
        context = {"C_LicProv" : id,
                   "M_LicProv_Nro": lic_provisional["M_LicProv_Nro"],
                    "N_Imagen_Base64": image_base_64,
                    "url_QR": url_QR,}
        
        template = get_template('licenciaProvisional.html')
        html = template.render(context = context)                        
    
        file_generate = pdfkit.from_string(html, False)
        response = HttpResponse(file_generate, content_type="application/pdf")
        file_name_download = "licenciaProvisional_{}.pdf".format(lic_provisional["M_LicProv_Nro"])
        print("*********************************************")
        print(file_name_download)
        response['Content-Disposition'] = "attachment; filename={}".format(file_name_download)

        # ********************* FIN GENERANDO PDF ********************* #

        return response

    return Response(
            data={"message": "No se encontro licencia provisional", "content": None},
            status=status.HTTP_400_BAD_REQUEST,
        )        