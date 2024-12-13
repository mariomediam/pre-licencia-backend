import os

from django.shortcuts import render
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponse

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from datetime import datetime


import pdfkit
import uuid

from .siaf import *

# Create your views here.
class MaestroDocumentoView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        data = sf_listar_maestro_documento()
        return Response(
            data={"message": "Lista de documentos", "content": data},
            status=status.HTTP_200_OK,
        )
    
class PersonaView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):        
        filtro = request.data.get("filtro")
        if not filtro:
            return Response(
                data={"message": "Filtro no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        data = sf_seleccionar_persona(filtro)        
        return Response(
            data={"message": "Lista de personas", "content": data},
            status=status.HTTP_200_OK,
        )
    

class ProveedorSIGAView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):        
        filtro = request.data.get("filtro")
        if not filtro:
            return Response(
                data={"message": "Filtro no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        data = sf_seleccionar_proveedor(filtro)        
        return Response(
            data={"message": "Lista de proveedores SIGA", "content": data},
            status=status.HTTP_200_OK,
        )
    

class SeleccionarExpedienteFase(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        ano_eje = request.query_params.get("anio")
        expediente = request.query_params.get("expediente")
        ciclo = request.query_params.get("ciclo")
        fase = request.query_params.get("fase")

        filters = {
            "ano_eje": ano_eje,
            "expediente": expediente,
            "ciclo": ciclo,
            "fase": fase,
        }

        if not ano_eje or not expediente or not ciclo or not fase:
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        data = sf_seleccionar_expediente_fase(**filters)        
        return Response(
            data={"message": "Expediente fase", "content": data},
            status=status.HTTP_200_OK,
        )
    
# sf_seleccionar_expediente_secuencia    

class SeleccionarExpedienteSecuencia(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        ano_eje = request.query_params.get("anio")
        expediente = request.query_params.get("expediente")
        secuencia = request.query_params.get("secuencia")
        correlativo = request.query_params.get("correlativo")

        filters = {
            "ano_eje": ano_eje,
            "expediente": expediente,
            "secuencia": secuencia,
            "correlativo": correlativo,
        }

        if not ano_eje or not expediente or not secuencia or not correlativo:
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        data = sf_seleccionar_expediente_secuencia(**filters)        
        return Response(
            data={"message": "Expediente secuencia", "content": data},
            status=status.HTTP_200_OK,
        )
    
def get_context_secuencia(params):
    data = sf_seleccionar_expediente_secuencia(**params)
    return data
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DownloadFormatoDevengadoController(request):    
    try:

        ano_eje = request.data.get("anio")
        expediente = request.data.get("expediente")
        secuencia = request.data.get("secuencia")
        correlativo = request.data.get("correlativo")
        retentions = request.data.get("retentions")
        login = request.user   
        fecha_print = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')                  

        if ano_eje and expediente and secuencia and correlativo and retentions:

            # ********************* INCIO HEADER PDF ********************* #                            
            
            template = get_template('formato-devengado-header.html')
            context = {"ANO_EJE" : ano_eje, "EXPEDIENTE" : expediente,}
            
            options = {
                'encoding': "UTF-8",                           
            }  

            page_header = template.render(context = context)
            header_template_path = os.path.join(settings.MEDIA_ROOT, 'reque-header' + str(uuid.uuid4()) + '.html')
            
            text_file = open(header_template_path, "w", encoding='utf-8')            
            text_file.write(page_header)
            text_file.close()

            # ********************* INCIO FOOTER PDF ********************* #
            
            template = get_template('formato-devengado-footer.html')

            context = {"login": login, "fecha_print": fecha_print}

            page_footer = template.render(context = context)
            
            footer_template_path = os.path.join(settings.MEDIA_ROOT, 'reque-footer' + str(uuid.uuid4()) + '.html')
            
            text_file = open(footer_template_path, "w", encoding='utf-8')            
            text_file.write(page_footer)
            text_file.close()

            

            # ********************* INCIO MAIN PDF ********************* #  
            filters = {
                "ano_eje": ano_eje,
                "expediente": expediente,
                "secuencia": secuencia,
                "correlativo": correlativo,
            }          
          
            context = sf_seleccionar_expediente_secuencia(**filters)        

            total_retentions = 0
            for retention in retentions:
                total_retentions += retention["value"]

            context["retentions"] = retentions
            context["total_retentions"] = total_retentions
            context["monto_final"] = context["MONTO_NACIONAL"] - total_retentions
            # print(context["total_retentions"])
            
            template = get_template('formato-devengado.html')            
            html = template.render(context = context)    
            
            options = {
                'page-size': 'A4',
                'margin-top': '2.0in',
                'margin-right': '0.25in',
                'margin-bottom': '0.50in',
                'margin-left': '0.25in',
                'encoding': "UTF-8",                           
                'footer-html': footer_template_path,    
                'header-html': header_template_path,
                'footer-font-size':'7',
                'footer-right': 'Pagina [page] de [topage]',
                           
            }        
                    
            file_generate = pdfkit.from_string(html, False, options=options)
            response = HttpResponse(file_generate, content_type="application/pdf")            
            file_name_download = "requerimiento{}-{}-{}-{}.pdf".format(ano_eje, expediente, secuencia, correlativo)            
            response['Content-Disposition'] = "attachment; filename={}".format(file_name_download)

            # ********************* FIN GENERANDO PDF ********************* #
            os.remove(header_template_path)
            os.remove(footer_template_path)


            return response

        else:
            return Response(
                data={
                    "message": "Faltan parametros",
                    "content": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        
        return Response(
            data={"message": str(e), "content": None},
            status=status.HTTP_404_NOT_FOUND,
        )         