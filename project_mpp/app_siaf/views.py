import os
import io

from django.shortcuts import render
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponse

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
        domicilio = carta.get("DOMICILIO", "")

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

    
    