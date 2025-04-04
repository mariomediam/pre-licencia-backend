import os
import locale

from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from datetime import datetime

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpRequest

import pandas as pd
from sqlalchemy import create_engine
import urllib

from .serializers import UploadFileSerializer
from .tesorero import *
from .models import *
from app_siaf.siaf import sf_seleccionar_registros

# Establecer la configuración regional a español
locale.setlocale(locale.LC_ALL, 'es_PE.UTF-8')

# PATH_TEMP ruta donde se guardaran los archivos de excel temporalmente
PATH_TEMP = os.path.join(os.path.dirname(__file__),"temp")

TABLE_NAME = {
    "SALDO INICIAL": "TRIBUTO_SALDO_INICIAL",
    "EMISION": "TRIBUTO_EMISION",
    "ALTAS": "TRIBUTO_ALTA",
    "BAJAS": "TRIBUTO_BAJA",
    "RECAUDACION": "TRIBUTO_RECAUDACION",
    "BENEFICIOS": "TRIBUTO_BENEFICIO"
}

DTYPE_TRIBUTOS = {
    "SALDO INICIAL": {'cod-contribuyente': str, 
                'nombre-contribuyente': str,
                'anio': int,
                'importe': float, 
                'cod-partida': str, 
                'nombre-partida': str,
                'cuenta-contable': str
    },
    "EMISION": {'cod-contribuyente': str, 
                'nombre-contribuyente': str,
                'cod-partida': str, 
                'nombre-partida': str,
                'importe': float, 
                'cuenta-contable': str},
    "ALTAS": {'fecha': datetime, 
              'cod-contribuyente': str, 
              'nombre-contribuyente': str, 
              'anio': int,
              'cod-partida': str, 
              'nombre-partida': str, 
              'importe': float, 
              'cuenta-contable': str},
    "BAJAS": {'fecha': datetime,
                'cod-contribuyente': str, 
                'nombre-contribuyente': str, 
                'anio': int,
                'cod-partida': str, 
                'nombre-partida': str, 
                'importe': float, 
                'cuenta-contable': str},
    "RECAUDACION": {'fecha': datetime,
                    'recibo': str,
                    'cod-contribuyente': str, 
                    'nombre-contribuyente': str, 
                    'cod-partida': str, 
                    'nombre-partida': str, 
                    'anio': int,
                    'importe': float, 
                    'cuenta-contable': str},
    "BENEFICIOS": {'cod-contribuyente': str, 
                    'nombre-contribuyente': str, 
                    'recibo': str,
                    'anio': int,
                    'cod-partida': str, 
                    'nombre-partida': str, 
                    'fecha': datetime,  
                    'base-legal': str,                 
                    'importe': float, 
                    'cuenta-contable': str},
    "CONCILIACION": {
                    'cod-contribuyente': str, 
                    'nombre-contribuyente': str,                    
                    'importe': float}                 
}

RENAME_COLUMNS = {
    "SALDO INICIAL": {'cod-contribuyente': 'C_SalIni_Contrib',
                'nombre-contribuyente': 'N_SalIni_Contrib',
                'anio': 'M_SalIni_Anio',
                'cod-partida': 'C_SalIni_Partida',
                'nombre-partida': 'N_SalIni_Partida',
                'importe': 'Q_SalIni_Monto',
                'cuenta-contable': 'C_SalIni_CtaCon'},                
    "EMISION": {'cod-contribuyente': 'C_Emision_Contrib',
                'nombre-contribuyente': 'N_Emision_Contrib',
                'cod-partida': 'C_Emision_Partida',
                'nombre-partida': 'N_Emision_Partida',
                'importe': 'Q_Emision_Monto',
                'cuenta-contable': 'C_Emision_CtaCon'},
    "ALTAS": {'fecha': 'D_Alta',
                'cod-contribuyente': 'C_Alta_Contrib',
                'nombre-contribuyente': 'N_Alta_Contrib',
                'anio': 'M_Alta_Anio',
                'cod-partida': 'C_Alta_Partida',
                'nombre-partida': 'N_Alta_Partida',
                'importe': 'Q_Alta_Monto',
                'cuenta-contable': 'C_Alta_CtaCon'},
    "BAJAS": {'fecha': 'D_Baja',
                'cod-contribuyente': 'C_Baja_Contrib',
                'nombre-contribuyente': 'N_Baja_Contrib',
                'anio': 'M_Baja_Anio',
                'cod-partida': 'C_Baja_Partida',
                'nombre-partida': 'N_Baja_Partida',
                'importe': 'Q_Baja_Monto',
                'cuenta-contable': 'C_Baja_CtaCon'},
    "RECAUDACION": {'fecha': 'D_Recaud',
                'recibo': 'M_Recaud_Recibo',
                'cod-contribuyente': 'C_Recaud_Contrib',
                'nombre-contribuyente': 'N_Recaud_Contrib',
                'cod-partida': 'C_Recaud_Partida',
                'nombre-partida': 'N_Reacud_Partida',
                'anio': 'M_Recaud_Anio',
                'importe': 'Q_Recaud_Monto',
                'cuenta-contable': 'C_Recaud_CtaCon'},
    "BENEFICIOS": {'cod-contribuyente': 'C_Benefi_Contrib',
                    'nombre-contribuyente': 'N_Benefi_Contrib',
                    'recibo': 'M_Benefi_Recibo',
                    'anio': 'M_Benefi_Anio',
                    'cod-partida': 'C_Benefi_Partida',
                    'nombre-partida': 'N_Benefi_Partida',
                    'fecha': 'D_Benefi_Pago',
                    'base-legal': 'N_Benefi_BasLeg',
                    'importe': 'Q_Benefi_Monto',
                    'cuenta-contable': 'C_Benefi_CtaCon'}

}


class UploadFileTributo(CreateAPIView):
    serializer_class = UploadFileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):

        file_name = "file_temp.xlsx"        

        type_tax_add = request.data.get("type", None)        

        dataArchivo = request.FILES.copy()
        dataArchivo["location"] = PATH_TEMP
        dataArchivo["file_name"] = file_name
        data = self.serializer_class(data=dataArchivo,allowed_extensions=['xls', 'xlsx'])

        if data.is_valid():
            file_name_upload = data.save()   
            
            df = convert_excel_to_panda(f"{PATH_TEMP}/{file_name_upload}", type_tax_add)
            num_records = len(df)
            df_to_bd(df, type_tax_add) 
            

            return Response(
                data={"message": f"Se han insertado {num_records} registros en la tabla {TABLE_NAME[type_tax_add]}", "content": None},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                data={"message": "Error al subir el archivo", "content": data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

def convert_excel_to_panda(file_path, type_tax):      
    df = pd.read_excel(file_path, index_col=None, dtype=DTYPE_TRIBUTOS[type_tax])  
    
    # Quitar espacios de la derecha e izquierda en columnas de tipo str
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # si columna anio esta vacia poner el valor de cero
    if "anio" in df.columns:
        df["anio"] = df["anio"].fillna(0).astype(int)
    
    return df

def df_to_bd(df, type_tax):
    # Configuración de la cadena de conexión a SQL Server
    server = os.environ.get("DB_HOST")
    database = "SIGA"
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    driver = 'ODBC Driver 17 for SQL Server'
    nombre_tabla = TABLE_NAME[type_tax]
    connection_string = f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}/{database}?driver={driver}"

    engine = create_engine(connection_string)

    # Renombra las columnas y agrega la columna C_anipre
    df = df.rename(columns=RENAME_COLUMNS[type_tax])    

    # Inserta los datos en la tabla
    df.to_sql(name=nombre_tabla, 
        con=engine, 
        if_exists='append', 
        index=False)

    # Cierra la conexión
    engine.dispose()

    # Fallo por ser muy lento
    # df = df.rename(columns=RENAME_COLUMNS[type_tax])   
    # print(df.head())
    # bulk_list = []
    # print("*********** 6 ***********")
    # for x in df.to_dict('records'):
    #     bulk_list.append(TributoEmisionModel(
    #         C_Archivo_id = x.get("C_Archivo"),
    #         C_Emision_Contrib = x.get("C_Emision_Contrib"),
    #         N_Emision_Contrib = x.get("N_Emision_Contrib"),
    #         C_Emision_Partida = x.get("C_Emision_Partida"),
    #         N_Emision_Partida = x.get("N_Emision_Partida"),
    #         Q_Emision_Monto = x.get("Q_Emision_Monto"),
    #         C_Emision_CtaCon = x.get("C_Emision_CtaCon"),
    #         D_Emision_FecDig = x.get("D_Emision_FecDig"),
    #         C_Usuari_Login = x.get("C_Usuari_Login"),
    #         N_Emision_PC = x.get("N_Emision_PC")
    #     ))
    # print("*********** 7 ***********")
    # TributoEmisionModel.objects.using("BDSIGA").bulk_create(bulk_list)


class TributoTipoOperacionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        type_tax = request.query_params.get("type", None)
        data = TributoSelect(type_tax)
        return Response(
            data={"message": "Lista de tributos", "content": data},
            status=status.HTTP_200_OK,
        )
    
class TributoArchivoView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        opcion = request.query_params.get("opcion")
        valor01 = request.query_params.get("valor01", None)
        valor02 = request.query_params.get("valor02", None)
        valor03 = request.query_params.get("valor03", None)

        if opcion is None:
            return Response(
                data={"message": "Error", "content": "Falta el parámetro 'opcion'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        data = TributoArchivoSelect(opcion, valor01, valor02, valor03)
        return Response(
            data={"message": "Lista de archivos", "content": data},
            status=status.HTTP_200_OK,
        )
    
    def post(self, request: Request):
        c_tip_ope = request.data.get("tipo")
        m_archivo_anio = request.data.get("anio", None)
        m_archivo_mes = request.data.get("mes", None)
        c_usuari_login = request.user.username        
        n_pc = request.META.get("REMOTE_ADDR")

        c_archivo = None
                
        try:            
            if c_tip_ope is None:
                return Response(
                    data={"message": "Error", "content": "Falta el parámetro 'tipo'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            type_tax_add = getNombreTipoOpeFin(c_tip_ope)

            if type_tax_add is None:
                return Response(
                    data={"message": f"No se encontró el tipo de operación {c_tip_ope}", "content": None},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            file_name = "file_temp.xlsx"        
            
            dataArchivo = request.FILES.copy()
            dataArchivo["location"] = PATH_TEMP
            dataArchivo["file_name"] = file_name
            data = UploadFileSerializer(data=dataArchivo,allowed_extensions=['xls', 'xlsx'])

            if data.is_valid():
                file_name_upload = data.save()   
                data = TributoInsertArchivo(c_tip_ope, m_archivo_anio, m_archivo_mes, c_usuari_login, n_pc)
                c_archivo = data.get("C_Archivo", None)
                
                
                df = convert_excel_to_panda(f"{PATH_TEMP}/{file_name_upload}", type_tax_add)
                df.insert(0, "C_Archivo", c_archivo)
                df = setFormatDf(df, type_tax_add, c_usuari_login = c_usuari_login, n_pc = n_pc)
                
                num_records = len(df)
                df_to_bd(df, type_tax_add) 

                os.remove(f"{PATH_TEMP}/{file_name_upload}")

                return Response(
                    data={"message": f"Se han insertado {num_records} registros", "content": None},
                    status=status.HTTP_201_CREATED,
                )

            else:
                return Response(
                    data={"message": "Error al subir el archivo", "content": data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        except Exception as e:
            if c_archivo is not None:
                TributoDeleteArchivo(c_archivo, c_usuari_login, n_pc)

            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def delete(self, request: Request, id=None):        
        c_archivo = id
        c_usuari_login = request.user.username        
        n_pc = request.META.get("REMOTE_ADDR")

        if c_archivo is None:
            return Response(
                data={"message": "Error", "content": "Falta el parámetro 'id'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            TributoDeleteArchivo(c_archivo, c_usuari_login, n_pc)
            return Response(
                data={"message": "Archivo eliminado", "content": None},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

def getNombreTipoOpeFin(c_tip_ope):
    data = TributoSelect(c_tip_ope)
    if len(data) > 0:
        return data[0]["N_TipOpe"]
    else:
        return None 
    
def setFormatDf(df, type_tax, **kwargs):

    if type_tax == "SALDO INICIAL":
        df["D_SalIni_FecDig"] = datetime.now()
        df["C_Usuari_Login"] = kwargs.get("c_usuari_login")
        df["N_SalIni_PC"] = kwargs.get("n_pc")

    if type_tax == "EMISION":
        df["D_Emision_FecDig"] = datetime.now()
        df["C_Usuari_Login"] = kwargs.get("c_usuari_login")
        df["N_Emision_PC"] = kwargs.get("n_pc")

    if type_tax == "ALTAS":
        df["D_Alta_FecDig"] = datetime.now()
        df["C_Usuari_Login"] = kwargs.get("c_usuari_login")
        df["N_Alta_PC"] = kwargs.get("n_pc")

    if type_tax == "BAJAS":
        df["D_Baja_FecDig"] = datetime.now()
        df["C_Usuari_Login"] = kwargs.get("c_usuari_login")
        df["N_Baja_PC"] = kwargs.get("n_pc")

    if type_tax == "RECAUDACION":
        df["D_Recaud_FecDig"] = datetime.now()
        df["C_Usuari_Login"] = kwargs.get("c_usuari_login")
        df["N_Recaud_PC"] = kwargs.get("n_pc")

    if type_tax == "BENEFICIOS":
        df["D_Benefi_FecDig"] = datetime.now()
        df["C_Usuari_Login"] = kwargs.get("c_usuari_login")
        df["N_Benefi_PC"] = kwargs.get("n_pc")
    
    return df

class TributoPeriodosDisponiblesView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        c_tip_ope = request.query_params.get("tipo", None)
        m_archivo_anio = request.query_params.get("anio", None)

        try:

            if c_tip_ope is None:
                return Response(
                    data={"message": "Error", "content": "Falta el parámetro 'tipo'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if m_archivo_anio is None and c_tip_ope != "01":
                return Response(
                    data={"message": "Error", "content": "Falta el parámetro 'anio'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if m_archivo_anio:
                m_archivo_anio = int(m_archivo_anio)

            data = TributoPeriodosDisponibles(c_tip_ope, m_archivo_anio)
            return Response(
                data={"message": "Lista de periodos disponibles", "content": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])        
def DownloadTributoArchivoView(request, id):    
    
    c_archivo = id

    if c_archivo is None:
        return Response(
            data={"message": "Error", "content": "Falta el parámetro 'id'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        sql = f"EXEC TributoArchivoSelectDetalle {c_archivo}"
        df = sql_to_pandas(sql)            
        df = df.drop(columns=["C_OpeFin", "C_Archivo"])
        name_file = getNameFile(c_archivo)
        full_path_file = f"{PATH_TEMP}/{name_file}.xlsx"
        df.to_excel(full_path_file, index=False)
        with open(full_path_file, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename={}".format(name_file)
        os.remove(full_path_file)



        return response
        
    except Exception as e:
        return Response(
            data={"message": str(e), "content": None},
            status=status.HTTP_400_BAD_REQUEST,
        )        
        

def sql_to_pandas(sql):    
    server = os.environ.get("DB_HOST")
    database = "SIGA"
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    driver = 'ODBC Driver 17 for SQL Server'
    connection_string = f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}/{database}?driver={driver}"


    engine = create_engine(connection_string)

    df = pd.read_sql(sql, engine)

    # Cierra la conexión
    engine.dispose()

    return df


def getNameFile(c_archivo):
    opcion = "02"
    tributo_archivo = TributoArchivoSelect(opcion, c_archivo)

    if len(tributo_archivo) == 0:
        return ""
    
    c_tip_ope = tributo_archivo[0]["C_TipOpe"]
    m_archivo_anio = tributo_archivo[0]["M_Archivo_Anio"]
    m_archivo_mes = tributo_archivo[0]["M_Archivo_Mes"]

    tipo_tributo = TributoSelect(c_tip_ope)

    if len(tipo_tributo) == 0:
        return ""
    
    nombre_tributo = tipo_tributo[0]["N_TipOpe"]

    name_file = f"{nombre_tributo}"

    if m_archivo_anio is not None:
        name_file = f"{name_file}_{m_archivo_anio}"

    if m_archivo_mes is not None:
        name_file = f"{name_file}_{m_archivo_mes}"

    return name_file

def actualizar_contrib_dict(contrib_dict, item, tipo):
    contrib_key = item[f"C_{tipo}_Contrib"].strip()
    tipo_tributo_key = item["C_TipOpe"]
    mes_key = item.get("M_Archivo_Mes")

    contrib = contrib_dict.setdefault(contrib_key, {
        "C_Contrib": contrib_key,
        "N_Contrib": item[f"N_{tipo}_Contrib"].strip(),
        "detalle": {}
    })

    tipo_tributo = contrib["detalle"].setdefault(tipo_tributo_key, {
        "C_TipOpe": tipo_tributo_key,
        "N_TipOpe": item["N_TipOpe"],
        "detalle": {} if mes_key else []
    })

    if mes_key:
        mes_detalle = tipo_tributo["detalle"].setdefault(mes_key, {"M_Archivo_Mes": mes_key,  "detalle": []})
        mes_detalle["detalle"].append(item)
    else:
        tipo_tributo["detalle"].append(item)

def getTributoSelectContrib(valor, anio):
    contrib_dict = {}

    # Simplificar la obtención de items y su procesamiento
    for tipo, funcion in [("SalIni", TributoSaldoInicialSelectContrib), 
                          ("Emision", TributoEmisionSelectContrib), 
                          ("Alta", TributoAltaSelectContrib), 
                          ("Baja", TributoBajaSelectContrib), 
                          ("Recaud", TributoRecaudacionSelectContrib), 
                          ("Benefi", TributoBeneficioSelectContrib)]:
        # items = funcion(valor) if tipo == "SalIni" else funcion(valor, anio)
        items = funcion(valor, anio)
        for item in items:
            actualizar_contrib_dict(contrib_dict, item, tipo)

    # Ordenar contribuciones
    sorted_contribs = sorted(contrib_dict.values(), key=lambda x: (locale.strxfrm(x['N_Contrib']), locale.strxfrm(x['C_Contrib'])))

    # Procesar y limpiar detalles
    for contrib in sorted_contribs:
        if "detalle" in contrib:
            for tipo_tributo, detalle in list(contrib["detalle"].items()): 
                if tipo_tributo not in ["01", "02"]:
                    detalle["detalle"] = list(detalle["detalle"].values())               
                    pass
            contrib["detalle"] = list(contrib["detalle"].values())

    return sorted_contribs


class TributoSelectContribView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        valor = request.query_params.get("valor", None)
        anio = request.query_params.get("anio", None)

        try:

            if valor is None:
                return Response(
                    data={"message": "Error", "content": "Falta el parámetro 'valor'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if anio is not None:
                anio = int(anio)

            data = getTributoSelectContrib(valor, anio)
            return Response(
                data={"message": "Lista de tributos", "content": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

class TributoOpeFinView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):       
        list_ope_fin = request.data.get("listOpeFin", None)
        c_usuari_login = request.user.username        
        n_pc = request.META.get("REMOTE_ADDR")

        if list_ope_fin is None:
            return Response(
                data={"message": "Error", "content": "Falta el listado a eliminar"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try: 
            with transaction.atomic():             
                for ope_fin in list_ope_fin:
                    c_ope_fin = ope_fin.get("C_OpeFin")
                    c_archivo = ope_fin.get("C_Archivo")
                    TributoOpeFinDelete(c_ope_fin, c_archivo, c_usuari_login, n_pc)
                
                return Response(
                    data={"message": "Operaciones financieras eliminadas exitosamente", "content": None},
                    status=status.HTTP_200_OK,
                )
            
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
    def post(self, request: Request):

        request_data = {key: request.data.get(key, None) for key in [
        "C_TipOpe", "D_Fecha", "C_Contrib", "N_Contrib", "C_Partida", "N_Partida",
        "M_Anio", "Q_Monto", "C_CtaCon", "M_Recibo", "N_BasLeg", "M_Archivo_Anio", "M_Archivo_Mes"
        ]}

        c_usuari_login = request.user.username
        n_pc = request.META.get("REMOTE_ADDR")

        # Mapeo de tipos de operación a funciones y argumentos
        operaciones = {
            "01": ("03", TributoSaldoInicialInsert, ["C_Archivo", "C_Contrib", "N_Contrib", "M_Anio", "Q_Monto", "C_Partida", "N_Partida", "C_CtaCon"]),
            "02": ("04", TributoEmisionInsert, ["C_Archivo", "C_Contrib", "N_Contrib", "C_Partida", "N_Partida", "Q_Monto", "C_CtaCon"]),
            "03": ("05", TributoAltaInsert, ["C_Archivo", "D_Fecha", "C_Contrib", "N_Contrib", "M_Anio", "C_Partida", "N_Partida", "Q_Monto", "C_CtaCon"]),
            "04": ("05", TributoBajaInsert, ["C_Archivo", "D_Fecha", "C_Contrib", "N_Contrib", "M_Anio", "C_Partida", "N_Partida", "Q_Monto", "C_CtaCon"]),
            "05": ("05", TributoRecaudacionInsert, ["C_Archivo", "D_Fecha", "M_Recibo", "C_Contrib", "N_Contrib", "C_Partida", "N_Partida", "M_Anio", "Q_Monto", "C_CtaCon"]),
            "06": ("05", TributoBeneficioInsert, ["C_Archivo", "C_Contrib", "N_Contrib", "M_Recibo", "M_Anio", "C_Partida", "N_Partida", "D_Fecha", "N_BasLeg", "Q_Monto", "C_CtaCon"])
        }
        
        c_tipope = request_data["C_TipOpe"]
        if c_tipope not in operaciones:
            return Response(data={"message": "Tipo de operación no válido", "content": None}, status=status.HTTP_400_BAD_REQUEST)

        archivo_tipo, funcion_insert, campos = operaciones[c_tipope]
        m_archivo_anio, m_archivo_mes = request_data["M_Archivo_Anio"], request_data["M_Archivo_Mes"]
        tributo_archivo = TributoArchivoSelect(archivo_tipo, c_tipope, m_archivo_anio, m_archivo_mes)

        if not tributo_archivo:
            return Response(data={"message": "No se encontró el archivo requerido", "content": None}, status=status.HTTP_400_BAD_REQUEST)

        c_archivo = tributo_archivo[0]["C_Archivo"]

        request_data["C_Archivo"] = c_archivo
        
        args = [request_data[campo] for campo in campos] + [c_usuari_login, n_pc]

        try:
            with transaction.atomic():
                funcion_insert(*args)
                return Response(data={"message": "Operación financiera insertada exitosamente", "content": None}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response(data={"message": str(e), "content": None}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request: Request, opeFinId: int, archivoId: int):

        request_data = {key: request.data.get(key, None) for key in [
        "D_Fecha", "C_Contrib", "N_Contrib", "C_Partida", "N_Partida",
        "M_Anio", "Q_Monto", "C_CtaCon", "M_Recibo", "N_BasLeg", 
        ]}

        c_ope_fin = opeFinId
        c_archivo = archivoId
        c_usuari_login = request.user.username
        n_pc = request.META.get("REMOTE_ADDR")
        request_data["C_OpeFin"] = c_ope_fin
       
        operaciones = {
            "01": (TributoSaldoInicialUpdate, ["C_OpeFin", "C_Contrib", "N_Contrib", "M_Anio", "Q_Monto", "C_Partida", "N_Partida", "C_CtaCon"]),
            "02": (TributoEmisionUpdate, ["C_OpeFin", "C_Contrib", "N_Contrib", "C_Partida", "N_Partida", "Q_Monto", "C_CtaCon"]),
            "03": (TributoAltaUpdate, ["C_OpeFin", "D_Fecha", "C_Contrib", "N_Contrib", "M_Anio", "C_Partida", "N_Partida", "Q_Monto", "C_CtaCon"]),
            "04": (TributoBajaUpdate, ["C_OpeFin", "D_Fecha", "C_Contrib", "N_Contrib", "M_Anio", "C_Partida", "N_Partida", "Q_Monto", "C_CtaCon"]),
            "05": (TributoRecaudacionUpdate, ["C_OpeFin", "D_Fecha", "M_Recibo", "C_Contrib", "N_Contrib", "C_Partida", "N_Partida", "M_Anio", "Q_Monto", "C_CtaCon"]),
            "06": (TributoBeneficioUpdate, ["C_OpeFin", "C_Contrib", "N_Contrib", "M_Recibo", "M_Anio", "C_Partida", "N_Partida", "D_Fecha", "N_BasLeg", "Q_Monto", "C_CtaCon"])
        }

        try:  

            tributo_archivo = TributoArchivoSelect("02", c_archivo)
            if len(tributo_archivo) == 0:
                raise Exception("No se encontró el archivo requerido")
            
            c_tipope = tributo_archivo[0]["C_TipOpe"]

            if c_tipope not in operaciones:
                return Response(data={"message": "Tipo de operación no válido", "content": None}, status=status.HTTP_400_BAD_REQUEST)
            
            funcion_update, campos = operaciones[c_tipope]

            args = [request_data[campo] for campo in campos] + [c_usuari_login, n_pc]

            with transaction.atomic():
                funcion_update(*args)
                return Response(data={"message": "Operación financiera actualizada exitosamente", "content": None}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                data={"message": e.args, "content": None},
                status=400,
            )
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])        
def DownloadTributoReporteView(request):    
    
    opcion = request.data.get("opcion", None)
    M_Archivo_Anio = request.data.get("M_Archivo_Anio", None)
    mes_hasta = request.data.get("mes_hasta", None)
    contrib = request.data.get("contrib", "")

    try:
        if opcion is None:
            return Response(
                data={"message": "Error", "content": "Falta el parámetro opcion"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if M_Archivo_Anio is None:
            return Response(
                data={"message": "Error", "content": "Falta el parámetro M_Archivo_Anio"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if mes_hasta is None:
            return Response(
                data={"message": "Error", "content": "Falta el parámetro mes_hasta"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        M_Archivo_Anio = int(M_Archivo_Anio)
        mes_hasta = int(mes_hasta)
        
        sql = ""
        if opcion == "01":
            sql = f"EXEC TributoContibuyentePartida {M_Archivo_Anio}, {mes_hasta}, '{contrib}'"
        elif opcion == "02":
            sql = f"EXEC TributoCuentasxCobrarContribuyente {M_Archivo_Anio}, {mes_hasta}, '{contrib}'"
        elif opcion == "03":
            sql = f"EXEC TributoCuentasxCobrarPartida {M_Archivo_Anio}, {mes_hasta}, '{contrib}'"

        df = sql_to_pandas(sql)     
        
        if "C_Contrib" in df.columns:
            df = df.rename(columns={"C_Contrib": "cod-contribuyente"})
        if "N_Contrib" in df.columns:
            df = df.rename(columns={"N_Contrib": "nombre-contribuyente"})
        
        if len(df) > 0 and opcion =="02" :                  
            df["Cuentas_por_cobrar"] = df.iloc[:, 2:].sum(axis=1)

        if len(df) > 0 and opcion =="03" :                  
            df["Cuentas_por_cobrar"] = df.iloc[:, 1:].sum(axis=1)

        if "Cuentas_por_cobrar" in df.columns:
            df["Cuentas_por_cobrar"] = pd.to_numeric(df["Cuentas_por_cobrar"], errors='coerce')
            df["Cuentas_por_cobrar"] = df["Cuentas_por_cobrar"].round(2)

        if len(contrib) == 0:            
            name_file = "Reporte"
            full_path_file = f"{PATH_TEMP}/{name_file}.xlsx"
            df.to_excel(full_path_file, index=False)
            with open(full_path_file, 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename={}".format(name_file)
            os.remove(full_path_file)

            return response
        else:            
            data = df.to_dict(orient="records")
            return Response(
                data={"message": "Reporte", "content": data},
                status=status.HTTP_200_OK,
            )
        
    except Exception as e:
        return Response(
            data={"message": str(e), "content": None},
            status=status.HTTP_400_BAD_REQUEST,
        )
    

class TributoConciliaView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        m_archivo_anio = request.data.get("anio", None)
        mes_hasta = request.data.get("mes", None)
        c_usuari_login = request.user.username        
        n_pc = request.META.get("REMOTE_ADDR")

        try:
        
            if m_archivo_anio is None:
                return Response(
                    data={"message": "Error", "content": "Falta el parámetro 'anio'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if m_archivo_anio:
                m_archivo_anio = int(m_archivo_anio)

            if mes_hasta:
                mes_hasta = int(mes_hasta)

            # Subiendo el archivo
            file_name = "file_temp.xlsx"        
            
            dataArchivo = request.FILES.copy()
            dataArchivo["location"] = PATH_TEMP
            dataArchivo["file_name"] = file_name
            data = UploadFileSerializer(data=dataArchivo,allowed_extensions=['xls', 'xlsx'])

            if data.is_valid():
                file_name_upload = data.save()   

                df_satp = convert_excel_to_panda(f"{PATH_TEMP}/{file_name_upload}", "CONCILIACION")
                
                os.remove(f"{PATH_TEMP}/{file_name_upload}")

                sql = f"EXEC TributoConciliacion {m_archivo_anio}, {mes_hasta}"

                df_mpp = sql_to_pandas(sql) 

                
                if "C_Contrib" in df_mpp.columns:
                    df_mpp = df_mpp.rename(columns={"C_Contrib": "cod-contribuyente"})
                if "N_Contrib" in df_mpp.columns:
                    df_mpp = df_mpp.rename(columns={"N_Contrib": "nombre-contribuyente"})
                if "Q_Monto" in df_mpp.columns:
                    df_mpp = df_mpp.rename(columns={"Q_Monto": "importe"})

                #  quitar espacios en blanco al inicio y final de columna cod-contribuyente
                df_mpp["cod-contribuyente"] = df_mpp["cod-contribuyente"].str.strip()
                df_satp["cod-contribuyente"] = df_satp["cod-contribuyente"].str.strip()


                # Merge de los dataframes

                df = pd.merge(df_satp, df_mpp, how="outer", on="cod-contribuyente", suffixes=("_satp", "_mpp"))
                
                df["importe_satp"] = df["importe_satp"].fillna(0)
                df["importe_mpp"] = df["importe_mpp"].fillna(0)
                

                df["diferencia"] = df["importe_satp"] - df["importe_mpp"]

                # print(df.head())

                name_file = "Reporte"
                full_path_file = f"{PATH_TEMP}/{name_file}.xlsx"
                df.to_excel(full_path_file, index=False)
                with open(full_path_file, 'rb') as excel_file:
                    response = HttpResponse(excel_file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response['Content-Disposition'] = "attachment; filename={}".format(name_file)
                os.remove(full_path_file)

                return response

             
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

class EjecucionDetalladaView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        search_sources = request.data.get("sources")
        desde = request.data.get("desde")
        hasta = request.data.get("hasta")
        ciclo = request.data.get("ciclo")
        fase = request.data.get("fase")
        secfun = request.data.get("meta")
        depen = request.data.get("depen")
        siga_prov = request.data.get("sigaprov")
        clapre = request.data.get("clasificador")
        fuefin = request.data.get("rubro")
        siga_plancon = request.data.get("sigaplancont")
        siga_exp = request.data.get("sigaexped")
        cp = request.data.get("cp")
        oper = request.data.get("operacion")
        scompro = request.data.get("scompro")
        obs = request.data.get("glosa")
        tipdoc = request.data.get("documento")
        docum = request.data.get("numerodoc")
        recurso = request.data.get("recurso")
        siga_exp_q = request.data.get("sigaprecomp")
        siaf_prov = request.data.get("siafprov")
        siaf_ctacte = request.data.get("siafctacte")
        siaf_certificado = request.data.get("siafcertificado")
        siaf_expediente = request.data.get("siafexped")
        tipo_reporte = request.data.get("tipo_reporte", "1")
        

        if search_sources is None or desde is None or hasta is None or ciclo is None:
            return Response(
                data={"message": "Error", "content": "Falta el parámetro 'desde', 'hasta' o 'ciclo'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            detailed_execution = {}
            if "siaf" in search_sources:                       
                detailed_execution["siaf"] = sf_seleccionar_registros(**{
                    "fecha1": desde,
                    "fecha2": hasta,
                    "ciclo": ciclo,
                    "fase": fase,
                    "rubro": fuefin,
                    "tipo_recurso": recurso,
                    "meta": secfun,
                    "tipo_operacion": oper,
                    "cod_doc": tipdoc,
                    "num_doc": docum,
                    "glosa": obs,
                    "clasificador": clapre,
                    "certificado": siaf_certificado,
                    "proveedor": siaf_prov,
                    "ctacte": siaf_ctacte,
                    "expediente": siaf_expediente,
                    "tipo_reporte": tipo_reporte
                })

            if "siga.net" in search_sources:
                detailed_execution["siga.net"] = SelectEjecucionDetallada(D_FECHA1=desde, D_FECHA2=hasta, C_CICLO=ciclo, C_FASE=fase, C_SECFUN=secfun, C_DEPEN=depen, C_PROV=siga_prov, C_CLAPRE=clapre, C_FUEFIN=fuefin, C_PLANCON=siga_plancon, C_EXPED_NRO=siga_exp, C_CP=cp, C_OPER=oper, SCOMPRO=scompro, T_OBS=obs, C_TIPDOC=tipdoc, C_DOCUM=docum, C_RECURSO=recurso, C_EXP_Q=siga_exp_q)

            return Response(
                data={"message": "Lista de ejecución detallada", "content": detailed_execution},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_400_BAD_REQUEST,
            )   


def format_sql_value(value):
    if value is None:
        return 'NULL'
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return value

@api_view(['POST'])
@permission_classes([IsAuthenticated])        
def DownloadDetailedExecutionView(request):    
    source = request.data.get("source")
    desde = request.data.get("desde")
    hasta = request.data.get("hasta")
    ciclo = request.data.get("ciclo")
    fase = request.data.get("fase")
    secfun = request.data.get("meta")
    depen = request.data.get("depen")
    siga_prov = request.data.get("sigaprov")
    clapre = request.data.get("clasificador")
    fuefin = request.data.get("rubro")
    siga_plancon = request.data.get("sigaplancont")
    siga_exp = request.data.get("sigaexped")
    cp = request.data.get("cp")
    oper = request.data.get("operacion")    
    obs = request.data.get("glosa")
    tipdoc = request.data.get("documento")
    docum = request.data.get("numerodoc")
    recurso = request.data.get("recurso")
    siga_exp_q = request.data.get("sigaprecomp")
    siaf_prov = request.data.get("siafprov")
    siaf_ctacte = request.data.get("siafctacte")
    siaf_certificado = request.data.get("siafcertificado")
    siaf_expediente = request.data.get("siafexped")
    tipo_reporte = request.data.get("tipo_reporte", "1")

    try:
        sql = ""

        

        if source == "siaf":
            sql = f"""
            SET NOCOUNT ON;

            DECLARE @fecha1 date = {format_sql_value(desde)}
            DECLARE @fecha2 date = {format_sql_value(hasta)}
            DECLARE @expediente varchar(10) = {format_sql_value(siaf_expediente)}
            DECLARE @ciclo char(1) = {format_sql_value(ciclo)}
            DECLARE @fase char(1) = {format_sql_value(fase)}
            DECLARE @rubro char(2) = {format_sql_value(fuefin)}
            DECLARE @tipo_recurso char(2) = {format_sql_value(recurso)}
            DECLARE @meta char(4) = {format_sql_value(secfun)}
            DECLARE @tipo_operacion char(2) = {format_sql_value(oper)}
            DECLARE @cod_doc char(3) = {format_sql_value(tipdoc)}
            DECLARE @num_doc varchar(20) = {format_sql_value(docum)}
            DECLARE @glosa varchar(200) = {format_sql_value(obs)}
            DECLARE @clasificador varchar(15) = {format_sql_value(clapre)}
            DECLARE @certificado varchar(15) = {format_sql_value(siaf_certificado)}
            DECLARE @proveedor varchar(100) = {format_sql_value(siaf_prov)}
            DECLARE @ctacte varchar(12) = {format_sql_value(siaf_ctacte)}
            DECLARE @tipo_reporte char(1) = {format_sql_value(tipo_reporte)}

            EXEC BDSIAF.dbo.sf_seleccionar_registros @fecha1=@fecha1, @fecha2=@fecha2, @expediente=@expediente, @ciclo=@ciclo, @fase=@fase, @rubro=@rubro, @tipo_recurso=@tipo_recurso, @meta=@meta, @tipo_operacion=@tipo_operacion, @cod_doc=@cod_doc, @num_doc=@num_doc, @glosa=@glosa, @clasificador=@clasificador, @certificado=@certificado, @proveedor=@proveedor, @ctacte=@ctacte, @tipo_reporte=@tipo_reporte
            """

            print(sql)

        if source == "siga.net":
            sql = f"""
            DECLARE @D_FECHA1 date = {format_sql_value(desde)}
            DECLARE @D_FECHA2 date = {format_sql_value(hasta)}
            DECLARE @C_CICLO char(1) = {format_sql_value(ciclo)}
            DECLARE @C_FASE char(1) = {format_sql_value(fase)}
            DECLARE @C_SECFUN varchar(50) = {format_sql_value(secfun)}
            DECLARE @C_DEPEN varchar(50) = {format_sql_value(depen)}
            DECLARE @C_PROV varchar(50) = {format_sql_value(siga_prov)}
            DECLARE @C_CLAPRE varchar(50) = {format_sql_value(clapre)}
            DECLARE @C_FUEFIN varchar(50) = {format_sql_value(fuefin)}
            DECLARE @C_PLANCON varchar(50) = {format_sql_value(siga_plancon)}
            DECLARE @C_OPER char(2) = {format_sql_value(oper)}            
            DECLARE @T_OBS varchar(50) = {format_sql_value(obs)}
            DECLARE @C_TIPDOC char(3) = {format_sql_value(tipdoc)}
            DECLARE @C_DOCUM varchar(50) = {format_sql_value(docum)}
            DECLARE @C_RECURSO char(2) = {format_sql_value(recurso)}
            DECLARE @C_EXP_Q char(10) = {format_sql_value(siga_exp_q)}
            DECLARE @C_EXPED_NRO varchar(50) = {format_sql_value(siga_exp)}
            
            EXEC SelectEjecucionDetallada @D_FECHA1=@D_FECHA1, @D_FECHA2=@D_FECHA2, @C_CICLO=@C_CICLO, @C_FASE=@C_FASE, @C_SECFUN=@C_SECFUN, @C_DEPEN=@C_DEPEN, @C_PROV=@C_PROV, @C_CLAPRE=@C_CLAPRE, @C_FUEFIN=@C_FUEFIN, @C_PLANCON=@C_PLANCON, @C_OPER=@C_OPER, @T_OBS=@T_OBS, @C_TIPDOC=@C_TIPDOC, @C_DOCUM=@C_DOCUM, @C_RECURSO=@C_RECURSO, @C_EXP_Q=@C_EXP_Q, 
            @C_EXPED_NRO = @C_EXPED_NRO
            """ 
            

        df = sql_to_pandas(sql)  

        if len(df) > 0:
            name_file = "Reporte"
            full_path_file = f"{PATH_TEMP}/{name_file}.xlsx"
            df.to_excel(full_path_file, index=False)
            with open(full_path_file, 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename={}".format(name_file)
            os.remove(full_path_file)

            return response

            
    except Exception as e:
        return Response(
            data={"message": str(e), "content": None},
            status=status.HTTP_400_BAD_REQUEST,
        )

    

