import os
import io
import requests
import urllib3

from django.shortcuts import render
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Sum
from decimal import Decimal
from django.db import transaction


from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from datetime import datetime
from decimal import Decimal

import pdfkit
import uuid
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Side, Border, PatternFill
from openpyxl.utils import get_column_letter


from .siaf import *
from app_deploy.views import number_to_word_currency, BuscarSunat
from .models import Sincronizacion, RegistroSincronizacion, ProyectoInversion, ProgramacionProyectoInversion
from .serializers import ProyectoInversionSerializer


RESOURCE_ID = "35bdc5b5-017c-42c1-ba20-8820bf1248b7"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    
def get_context_secuencia(data, retentions):
    total_retentions = 0
    for retention in retentions:
        total_retentions += retention["value"]

    total_retentions_decimal = Decimal(str(total_retentions))
    
    monto_final = data["MONTO_NACIONAL"] - total_retentions_decimal
    
    data["retentions"] = retentions
    data["total_retentions"] = total_retentions_decimal
    data["monto_final"] = monto_final
    data["monto_final_text"] = number_to_word_currency(monto_final).upper()
    return data

def correct_supplier_name(data):    
    nro_ruc = data.get("RUC", "")
    if nro_ruc:
        filters = {
            "nro_ruc": nro_ruc
        }
        
        result = sf_seleccionar_sigamef_contratista(**filters)
        if result:
            data["NOMBRE"] = result.get("NOMBRE_PROV", "")
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

            data = sf_seleccionar_expediente_secuencia(**filters)  

            if not data["NOMBRE"]:
                data = correct_supplier_name(data)
            
            context = get_context_secuencia(data, retentions)   

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
    

class ProcesoActualizarRegistroView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):        
        ano_eje = request.data.get("anio")
        expediente = request.data.get("expediente")

        print("Ingreso *************")

        if not ano_eje or not expediente:
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )    
        
        try:
            filters = {
            "ano_eje": ano_eje,
            "expediente": expediente,
            }

            sf_proceso_actualizar_01_registro(**filters)        
            return Response(
                data={"message": "Proceso actualizar registro", "content": "Expediente migrado exitosamente"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        
class BuscarCartaOrdenView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):        
        cod_doc = request.data.get("codigo")
        num_doc = request.data.get("numero")

        if not cod_doc or not num_doc:
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )    

        try:
            filters = {
                "cod_doc": cod_doc,
                "num_doc": num_doc,
            }

            data = sf_buscar_carta_orden(**filters)        
            return Response(
                data={"message": "Carta orden", "content": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DownloadCartaOrdenFideicomisoController(request):    
    try:
        cartas = request.data.get("cartas")

        if not cartas:
            return Response(
                data={"message": "Faltan parametros"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        login = request.user

        cartas = get_domicilio_carta_orden(cartas)

        output = create_excel_carta_orden(cartas)
        
        # Crear la respuesta HTTP con el contenido del archivo Excel
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="reporte.xlsx"'
        return response
    
    except Exception as e:
        return Response(
            data={"message": str(e), "content": None},
            status=status.HTTP_404_NOT_FOUND,
        )

def create_excel_carta_orden(cartas):
    # Crear un nuevo libro de Excel y una hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

   # -- Fila 1: Título principal --
    ws.merge_cells("A1:H1")
    ws["A1"] = "FIDEICOMISO MUNICIPALIDAD PROVINCIAL DE PIURA - MINAM"    

    # -- Fila 2: Subtítulo (RUC) --
    ws.merge_cells("A2:H2")
    ws["A2"] = "RUC 20154477374"

    # quiero que la celda a1 tenga color de fondo gris y color de texto blanco
    for cell in ["A1", "A2"]:
        ws[cell].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
        ws[cell].font = Font(color="FFFFFF")

    # -- Fila 3: Encabezados de columnas --
    headers = [
        "OFICIO",            # A
        "N° DE ORDEN PAGO",  # B
        "BENEFICIARIO / MONTO EN LETRAS",  # C
        "N° DE CUENTA/CCI",  # D
        "TIPO DE CUENTA",    # E
        "BANCO",             # F
        "MONTO",             # G
        "CONCEPTO DE PAGO"   # H
    ]

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_num, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Ajustar anchos de columna
    col_widths = [8, 18, 40, 25, 15, 15, 12, 50]  # A-H
    for i, width in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width

    # Fila a partir de la cual empezaremos a escribir los datos
    start_row = 4

    for carta in cartas:
        # Por cada 'carta', vamos a usar 5 filas
        # -> Fusionar las celdas de OFICIO (A) para 4 filas
        ws.merge_cells(start_row=start_row, end_row=start_row+3, 
                       start_column=1, end_column=1)
        # -> Fusionar las celdas de ORDEN DE PAGO (B) para 4 filas
        ws.merge_cells(start_row=start_row, end_row=start_row+3, 
                       start_column=2, end_column=2)
        # -> Fusionar las celdas de CONCEPTO DE PAGO (H) para 4 filas
        ws.merge_cells(start_row=start_row, end_row=start_row+3, 
                       start_column=8, end_column=8)

        # OFICIO (ejemplo fijo o en blanco)
        oficio_value = ""  # o "49"
        ws.cell(row=start_row, column=1, value=oficio_value)
        ws.cell(row=start_row, column=1).alignment = Alignment(vertical="top")

        # ORDEN DE PAGO (ejemplo fijo o en blanco)
        orden_pago_value = carta.get("NUM_DOC", "")
        ws.cell(row=start_row, column=2, value=orden_pago_value)
        ws.cell(row=start_row, column=2).alignment = Alignment(vertical="top")

        # CONCEPTO DE PAGO
        glosa = carta.get("GLOSA", "")
        ws.cell(row=start_row, column=8, value=glosa)
        ws.cell(row=start_row, column=8).alignment = Alignment(
            wrap_text=True,
            vertical="top"
        )

        # Extraemos datos del "carta"
        proveedor = carta.get("NOMBRE_PROVEEDOR", "")
        ruc = carta.get("RUC", "")
        monto_numerico = carta.get("MONTO_NACIONAL", 0.0)
        monto_en_letras = f"SON: {number_to_word_currency(monto_numerico).upper()}"
        domicilio = f"DOMICIO LEGAL: {carta.get('DOMICILIO', '')}" 

        # N° CUENTA / CCI
        cci = carta.get("CCI", "")
        # TIPO DE CUENTA (ejemplo: "CORRIENTE")
        tipo_cuenta = carta.get("NOMBRE_CUENTA_CTE", "")
        # BANCO
        banco = carta.get("NOMBRE_BANCO", "")
        # MONTO (col G)
        monto = monto_numerico

        # -- Llenar 4 filas (columnas C-G) --

        # 1) Fila principal: Proveedor (col C), CCI (D), tipo cuenta (E), banco (F), monto (G)
        row_proveedor = start_row
        ws.cell(row=row_proveedor, column=3, value=proveedor)         
        ws.cell(row=row_proveedor, column=4, value=cci)
        ws.cell(row=row_proveedor, column=5, value=tipo_cuenta)
        ws.cell(row=row_proveedor, column=6, value=banco)
        celda_monto = ws.cell(row=row_proveedor, column=7, value=monto)
        celda_monto.number_format = '#,##0.00'


        # 2) Fila: Monto en letras (col C)
        row_monto_letras = start_row + 1        
        ws.merge_cells(F"C{row_monto_letras}:G{row_monto_letras}")
        ws.cell(row=row_monto_letras, column=3, value=monto_en_letras)

        # 3) Fila: DNI/RUC (col C)
        row_ruc = start_row + 2
        ws.merge_cells(F"C{row_ruc}:G{row_ruc}")
        ws.cell(row=row_ruc, column=3, value=f"DNI/RUC: {ruc}")

        # 4) Fila: Domicilio (col C)
        row_domicilio = start_row + 3
        ws.merge_cells(F"C{row_domicilio}:G{row_domicilio}")
        ws.cell(row=row_domicilio, column=3, value=domicilio)

        # Ajustes de alineación / wrap text en las celdas de col C
        for r in range(start_row, start_row + 4):
            cell_c = ws.cell(row=r, column=3)
            cell_c.alignment = Alignment(wrap_text=True, vertical="top")

        for col in range(4, 8):
            ws.cell(row=start_row, column=col).alignment = Alignment(wrap_text=True, vertical="top")

        # Ajustar altura de las filas
        for r in range(start_row, start_row + 4):
            # Cada fila un poco más alta para soportar wrap
            ws.row_dimensions[r].height = 22

        # Avanzar 4 filas para la siguiente 'carta'
        start_row += 4
    
    ws.merge_cells(start_row=start_row, end_row=start_row, start_column=1, end_column=3)
    ws.cell(row=start_row, column=1).alignment = Alignment(wrap_text=True, vertical="bottom")

    ws.merge_cells(start_row=start_row, end_row=start_row, start_column=4, end_column=6)
    ws.cell(row=start_row, column=4).alignment = Alignment(wrap_text=True, vertical="bottom")

    ws.merge_cells(start_row=start_row, end_row=start_row, start_column=7, end_column=8)
    ws.cell(row=start_row, column=7).alignment = Alignment(wrap_text=True, vertical="center")

    cell_values = {
    1: "2/ Firma autorizada",
    4: "2/ Firma autorizada",
    7: ("1/ Toda la información sobre los datos de los fideicomisarios indicada en las instrucciones de transferencia, es de responsabilidad única y exclusiva del Fideicomitente. Estas transferencias de fondos, están relacionadas a la finalidad del fideicomiso.\n"
        "2/ Dobles firmas registradas en el Banco de la Nación.")
    }

    for col, value in cell_values.items():
        celda = ws.cell(row=start_row, column=col, value=value)
        celda.font = Font(size=8)        

    ws.row_dimensions[start_row].height = 120

    # Agregar un borde fino a todas las celdas, desde la celda A1 hasta la última celda con datos
    thin_side = Side(style='thin', color="000000")
    thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    for row in ws.iter_rows(min_row=1, max_row=start_row, min_col=1, max_col=8):
        for cell in row:
            cell.border = thin_border

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)  # Reiniciar la posición al inicio
    return output

def get_domicilio_carta_orden(cartas):

    domicilios_cache = {}
    
    for carta in cartas:
        ruc = carta.get("RUC", "")
        if not ruc:
            carta["DOMICILIO"] = ""
            continue
        
        if ruc not in domicilios_cache:
            resultado = BuscarSunat(ruc)            
            domicilio = f"{resultado.get('desc_tipvia', '').strip()} {resultado.get('ddp_nomvia', '').strip()} {resultado.get('ddp_numer1', '')} {resultado.get('ddp_nomzon', '').strip()} {resultado.get('desc_dep', '').strip()} - {resultado.get('desc_prov', '').strip()} - {resultado.get('desc_dist', '').strip()}".strip()
            domicilios_cache[ruc] = domicilio
        else:
            domicilio = domicilios_cache[ruc]
        
        # Asignar el domicilio obtenido a la carta
        carta["DOMICILIO"] = domicilio
    
    return cartas


class SincroGastoDiario(RetrieveAPIView):
   permission_classes = [IsAuthenticated]

   def get(self, request: Request):
      try:
        # Crear el objeto Sincronizacion antes de llamar a la API
        sinc = Sincronizacion.objects.create()

        ultima_actualizacion = getLastDataUpdate()
        
        # Obtener datos de la API
        data = getGastoDiario()

        # Pasar el objeto sincronizacion a la función saveGastoDiario
        saveGastoDiario(data, sinc, ultima_actualizacion)

        return Response(
            data={"message": "Sincronización completada exitosamente", "content": sinc.idSincro},
            status=status.HTTP_200_OK,
        )
                  
      except Exception as e:               
        return Response(
            data={"message": str(e), "content": None},
            status=status.HTTP_404_NOT_FOUND,
        )     
        

def getGastoDiario():   

      sql = (
         'SELECT * '
         'FROM "35bdc5b5-017c-42c1-ba20-8820bf1248b7" '
         "WHERE \"SEC_EJEC\" = '301529' "            
      )

      resp = requests.get(
         'https://api.datosabiertos.mef.gob.pe/DatosAbiertos/v1/datastore_search_sql',
         params={'sql': sql}
      )
      
      return resp.json()


def saveGastoDiario(gasto_diario, sinc, ultima_actualizacion):
    """
    Guarda en BD los registros de gasto diario traídos desde la API.
    Usa el objeto Sincronizacion creado previamente.
    """
    try:
        registros = gasto_diario.get('records', [])
        fila_error = None

        # Insertar cada fila en RegistroSincronizacion
        for fila in registros:
            fila_error = fila
            RegistroSincronizacion.objects.create(
                sincronizacion=sinc,
                ano_eje=fila.get('ANO_EJE'),
                mes_eje=fila.get('MES_EJE'),
                nivel_gobierno=fila.get('NIVEL_GOBIERNO'),
                nivel_gobierno_nombre=fila.get('NIVEL_GOBIERNO_NOMBRE'),
                sector=fila.get('SECTOR'),
                sector_nombre=fila.get('SECTOR_NOMBRE'),
                pliego=fila.get('PLIEGO'),
                pliego_nombre=fila.get('PLIEGO_NOMBRE'),
                sec_ejec=fila.get('SEC_EJEC'),
                ejecutora=fila.get('EJECUTORA'),
                ejecutora_nombre=fila.get('EJECUTORA_NOMBRE'),
                departamento_ejecutora=fila.get('DEPARTAMENTO_EJECUTORA'),
                departamento_ejecutora_nombre=fila.get('DEPARTAMENTO_EJECUTORA_NOMBRE'),
                provincia_ejecutora=fila.get('PROVINCIA_EJECUTORA'),
                provincia_ejecutora_nombre=fila.get('PROVINCIA_EJECUTORA_NOMBRE'),
                distrito_ejecutora=fila.get('DISTRITO_EJECUTORA'),
                distrito_ejecutora_nombre=fila.get('DISTRITO_EJECUTORA_NOMBRE'),
                sec_func=fila.get('SEC_FUNC'),
                programa_ppto=fila.get('PROGRAMA_PPTO'),
                programa_ppto_nombre=fila.get('PROGRAMA_PPTO_NOMBRE'),
                tipo_act_proy=fila.get('TIPO_ACT_PROY'),
                tipo_act_proy_nombre=fila.get('TIPO_ACT_PROY_NOMBRE'),
                producto_proyecto=fila.get('PRODUCTO_PROYECTO'),
                producto_proyecto_nombre=fila.get('PRODUCTO_PROYECTO_NOMBRE'),
                actividad_accion_obra=fila.get('ACTIVIDAD_ACCION_OBRA'),
                actividad_accion_obra_nombre=fila.get('ACTIVIDAD_ACCION_OBRA_NOMBRE'),
                funcion=fila.get('FUNCION'),
                funcion_nombre=fila.get('FUNCION_NOMBRE'),
                division_funcional=fila.get('DIVISION_FUNCIONAL'),
                division_funcional_nombre=fila.get('DIVISION_FUNCIONAL_NOMBRE'),
                grupo_funcional=fila.get('GRUPO_FUNCIONAL'),
                grupo_funcional_nombre=fila.get('GRUPO_FUNCIONAL_NOMBRE'),
                meta=fila.get('META'),
                finalidad=fila.get('FINALIDAD'),
                meta_nombre=fila.get('META_NOMBRE'),
                departamento_meta=fila.get('DEPARTAMENTO_META'),
                departamento_meta_nombre=fila.get('DEPARTAMENTO_META_NOMBRE'),
                fuente_financiamiento=fila.get('FUENTE_FINANCIAMIENTO'),
                fuente_financiamiento_nombre=fila.get('FUENTE_FINANCIAMIENTO_NOMBRE'),
                rubro=fila.get('RUBRO'),
                rubro_nombre=fila.get('RUBRO_NOMBRE'),
                tipo_recurso=fila.get('TIPO_RECURSO'),
                tipo_recurso_nombre=fila.get('TIPO_RECURSO_NOMBRE'),
                categoria_gasto=fila.get('CATEGORIA_GASTO'),
                categoria_gasto_nombre=fila.get('CATEGORIA_GASTO_NOMBRE'),
                tipo_transaccion=fila.get('TIPO_TRANSACCION'),
                generica=fila.get('GENERICA'),
                generica_nombre=fila.get('GENERICA_NOMBRE'),
                subgenerica=fila.get('SUBGENERICA'),
                subgenerica_nombre=fila.get('SUBGENERICA_NOMBRE'),
                subgenerica_det=fila.get('SUBGENERICA_DET'),
                subgenerica_det_nombre=fila.get('SUBGENERICA_DET_NOMBRE'),
                especifica=fila.get('ESPECIFICA'),
                especifica_nombre=fila.get('ESPECIFICA_NOMBRE'),
                especifica_det=fila.get('ESPECIFICA_DET'),
                especifica_det_nombre=fila.get('ESPECIFICA_DET_NOMBRE'),
                monto_pia=fila.get('MONTO_PIA'),
                monto_pim=fila.get('MONTO_PIM'),
                monto_certificado=fila.get('MONTO_CERTIFICADO'),
                monto_comprometido_anual=fila.get('MONTO_COMPROMETIDO_ANUAL'),
                monto_comprometido=fila.get('MONTO_COMPROMETIDO'),
                monto_devengado=fila.get('MONTO_DEVENGADO'),
                monto_girado=fila.get('MONTO_GIRADO'),
            )
        
        # Éxito
        sinc.comentarios = f'Sincronización exitosa ({len(registros)} registros).'
        sinc.exitoso = True
    except Exception as e:
        print("************** error ***********")
        print(fila_error)
        # Cualquier excepción se graba en comentarios
        sinc.comentarios = f'Error durante sincronización: {e}'
        sinc.exitoso = False        
    finally:
        # Marcar fecha_fin y guardar
        #sinc.fecha_fin = timezone.now()
        sinc.fecha_fin = datetime.now()
        sinc.ultima_actualizacion = ultima_actualizacion
        sinc.save()


def getLastDataUpdate(resource_id = RESOURCE_ID):
   
   url = "https://datosabiertos.mef.gob.pe/Rest/PortalWebRecursoDetalle/v1.0/getRecursoDetalle"
   
   # Datos para el body de la petición
   payload = {
       "dataset": "presupuesto-y-ejecucion-de-gasto",
       "id_recurso": resource_id
   }
   
   # Headers para la petición
   headers = {
       'Content-Type': 'application/json'
   }

   try:
       response = requests.post(
           url,
           json=payload,
           headers=headers,
           verify=False  # Deshabilitar verificación SSL
       )
       response.raise_for_status()  # Verificar si hay errores HTTP
       
       # Obtener el JSON de la respuesta
       data = response.json()
       
       # Obtener el valor de resource_last_modified
       last_modified = data.get('resource_detail', {}).get('resource_last_modified')
              
       return last_modified
       
   except requests.exceptions.SSLError as e:
       print(f"Error SSL: {e}")
       raise Exception(f"Error de SSL: {str(e)}")
   except requests.exceptions.RequestException as e:
       print(f"Error en la petición: {e}")
       raise Exception(f"Error en la petición: {str(e)}")
   except Exception as e:
       print(f"Error inesperado: {e}")
       raise Exception(f"Error inesperado: {str(e)}")


def getLastSincro():
    return Sincronizacion.objects.filter(
    exitoso=True
    ).order_by('-idSincro').first()

def getLastSincroByAnoEjecutora(ano_eje, sec_ejec):
    """
    Obtiene la última sincronización exitosa para un año y ejecutora específicos.
    
    Args:
        ano_eje (str): Año de ejecución
        sec_ejec (str): Código de la ejecutora
        
    Returns:
        Sincronizacion: Objeto de la última sincronización exitosa o None si no existe
    """
    return Sincronizacion.objects.filter(
        registros__ano_eje=ano_eje,
        registros__sec_ejec=sec_ejec,
        exitoso=True
    ).order_by('-idSincro').first()

class UltimaSincronizacionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            ano_eje = request.query_params.get('ano_eje')
            sec_ejec = request.query_params.get('sec_ejec')

            if not ano_eje or not sec_ejec:
                return Response(
                    data={"message": "Faltan parámetros ano_eje o sec_ejec"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            sincronizacion = Sincronizacion.obtener_ultima_sincronizacion_completa(ano_eje, sec_ejec)

            if not sincronizacion:
                return Response(
                    data={"message": "No se encontró sincronización exitosa", "content": None},
                    status=status.HTTP_200_OK
                )

            return Response(
                data={
                    "message": "Última sincronización encontrada",
                    "content": {
                        "idSincro": sincronizacion.idSincro,
                        "fecha_inicio": sincronizacion.fecha_inicio,
                        "fecha_fin": sincronizacion.fecha_fin,
                        "ultima_actualizacion": sincronizacion.ultima_actualizacion,
                        "comentarios": sincronizacion.comentarios,
                        "exitoso": sincronizacion.exitoso
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProgProyectosInversionMensualView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            ano_eje = request.query_params.get('ano_eje')
            mes_eje = request.query_params.get('mes_eje')
            sec_ejec = request.query_params.get('sec_ejec')

            if not all([ano_eje, mes_eje, sec_ejec]):
                return Response(
                    data={"message": "Faltan parámetros requeridos", "content": None},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
          
            
            # Obtener la última sincronización
            ultima_sincro = Sincronizacion.obtener_ultima_sincronizacion_completa(ano_eje, sec_ejec)
            
            if not ultima_sincro:
                return Response(
                    data={"message": "No se encontró sincronización exitosa", "content": []},
                    status=status.HTTP_200_OK
                )
            
            filters = {
                "ano_eje": ano_eje,
                "mes_eje": mes_eje,
                "sec_ejec": sec_ejec,
                "sincronizacion_id": ultima_sincro.idSincro
            }
            
            result = select_protectos_con_gasto_mensual(**filters)

            return Response(
                data={
                    "message": "Proyectos de inversión encontrados",
                    "content": result
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


def obtener_producto_proyecto(ano_eje: float, producto_proyecto: float) -> dict:
    """
    Obtiene la información de un producto/proyecto específico para un año dado.
    
    Args:
        ano_eje (float): Año de ejecución
        producto_proyecto (float): Código del producto/proyecto
        
    Returns:
        dict: Diccionario con la información del producto/proyecto o None si no se encuentra
    """
    registro = RegistroSincronizacion.objects.filter(
        ano_eje=ano_eje,
        producto_proyecto=producto_proyecto
    ).values('ano_eje', 'producto_proyecto', 'producto_proyecto_nombre').first()
    
    return registro


# CREAR UNA VISTA GET PARA OBTENER EL PRODUCTO PROYECTO
class ProductoProyectoNombreView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            ano_eje = request.query_params.get('ano_eje')
            producto_proyecto = request.query_params.get('producto_proyecto')

            if not ano_eje or not producto_proyecto:
                return Response(
                    data={"message": "Faltan parámetros requeridos", "content": None},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            result = obtener_producto_proyecto(ano_eje, producto_proyecto)
            return Response(
                data={
                    "message": "Proyectos de inversión encontrados",
                    "content": result
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def obtener_ultima_sincronizacion_por_anio(ano_eje: float) -> int:
    """
    Obtiene el ID de la última sincronización exitosa para un año específico.
    
    Args:
        ano_eje (float): Año de ejecución
        
    Returns:
        int: ID de la última sincronización exitosa o None si no se encuentra
    """
    ultima_sincronizacion = Sincronizacion.objects.filter(
        registros__ano_eje=ano_eje,
        exitoso=True
    ).order_by('-idSincro').first()
    
    return ultima_sincronizacion.idSincro if ultima_sincronizacion else None


class UltimaSincronizacionAnioView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        ano_eje = request.query_params.get('ano_eje')

        if not ano_eje:
            return Response(
                data={"message": "Faltan parámetros requeridos", "content": None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        id_sincro = obtener_ultima_sincronizacion_por_anio(ano_eje)

        return Response(
            data={"message": "Última sincronización encontrada", "content": id_sincro},
            status=status.HTTP_200_OK
        )




def obtener_resumen_producto_proyecto(producto_proyecto: Decimal, id_sincro: int) -> dict:
    """
    Obtiene el resumen de montos para un producto/proyecto específico de una sincronización.
    
    Args:
        producto_proyecto (Decimal): Código del producto/proyecto
        id_sincro (int): ID de la sincronización
        
    Returns:
        dict: Diccionario con los montos resumidos o None si no se encuentra
    """
    resultado = RegistroSincronizacion.objects.filter(
        sincronizacion_id=id_sincro,
        producto_proyecto=producto_proyecto
    ).values(
        'ano_eje',
        'producto_proyecto'
    ).annotate(
        MONTO_PIA=Sum('monto_pia'),
        MONTO_PIM=Sum('monto_pim'),
        MONTO_CERTIFICADO=Sum('monto_certificado'),
        MONTO_COMPROMETIDO_ANUAL=Sum('monto_comprometido_anual'),
        MONTO_COMPROMETIDO=Sum('monto_comprometido'),
        MONTO_DEVENGADO=Sum('monto_devengado'),
        MONTO_GIRADO=Sum('monto_girado')
    ).order_by('ano_eje', 'producto_proyecto').first()
    
    return resultado



class ResumenProductoProyectoView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        producto_proyecto = request.query_params.get('producto_proyecto')
        ano_eje = request.query_params.get('ano_eje')

        if not producto_proyecto or not ano_eje:
            return Response(
                data={"message": "Faltan parámetros requeridos", "content": None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        id_sincro = obtener_ultima_sincronizacion_por_anio(ano_eje)

        resumen = obtener_resumen_producto_proyecto(producto_proyecto, id_sincro)

        return Response(
            data={"message": "Resumen encontrado", "content": resumen},
            status=status.HTTP_200_OK
        )
    


# {
#     "ano_eje": 2025,
#     "c_proinv_codigo": "2331918",
#     "n_proinv_nombre": "MEJORAMIENTO DEL SERVICIO DE TRANSITABILIDAD PEATONAL Y VEHICULAR DE LA UPIS LOS ANGELES EN EL DISTRITO DE PIURA, PROVINCIA DE PIURA - PIURA",
#     "programacion": [
#         {
#             "m_prgpro_mes": 1,
#             "q_prgpro_financ": 100,
#             "p_prgpro_fisica": 1
#         },
#         {
#             "m_prgpro_mes": 2,
#             "q_prgpro_financ": 200,
#             "p_prgpro_fisica": 2
#         },
#         {
#             "m_prgpro_mes": 3,
#             "q_prgpro_financ": 300,
#             "p_prgpro_fisica": 3
#         },
#         {
#             "m_prgpro_mes": 4,
#             "q_prgpro_financ": 400,
#             "p_prgpro_fisica": 4
#         },
#         {
#             "m_prgpro_mes": 5,
#             "q_prgpro_financ": 500,
#             "p_prgpro_fisica": 5
#         },
#         {
#             "m_prgpro_mes": 6,
#             "q_prgpro_financ": 600,
#             "p_prgpro_fisica": 6
#         },
#         {
#             "m_prgpro_mes": 7,
#             "q_prgpro_financ": 700,
#             "p_prgpro_fisica": 7
#         },
#         {
#             "m_prgpro_mes": 8,
#             "q_prgpro_financ": 800,
#             "p_prgpro_fisica": 8
#         },
#         {
#             "m_prgpro_mes": 9,
#             "q_prgpro_financ": 900,
#             "p_prgpro_fisica": 9
#         },
#         {
#             "m_prgpro_mes": 10,
#             "q_prgpro_financ": 1000,
#             "p_prgpro_fisica": 10
#         },
#         {
#             "m_prgpro_mes": 11,
#             "q_prgpro_financ": 1100,
#             "p_prgpro_fisica": 11
#         },
#         {
#             "m_prgpro_mes": 12,
#             "q_prgpro_financ": 1200,
#             "p_prgpro_fisica": 34
#         }
#     ]
# }


# Dado el JSON anterior, se debe grabar el registro en las tablas ProyectoInversion y ProgramacionProyectoInversion

class ProyectoInversionView(CreateAPIView):    
    permission_classes = [IsAuthenticated]
    serializer_class = ProyectoInversionSerializer

    def post(self, request: Request):

        data = request.data
        data['c_usuari_login'] = request.user.username
        data['n_proinv_pc'] = request.META.get('REMOTE_ADDR')

        with transaction.atomic():
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                proyecto = serializer.instance
                print(proyecto.c_proinv)

                for programacion in data['programacion']:
                    
                    programacion['proyecto'] = proyecto
                    programacion['c_usuari_login'] = request.user.username
                    programacion['n_prgpro_pc'] = request.META.get('REMOTE_ADDR')

                    ProgramacionProyectoInversion.objects.create(**programacion)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    