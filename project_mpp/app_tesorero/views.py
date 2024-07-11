import os
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from datetime import datetime

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

import pandas as pd
from sqlalchemy import create_engine
import urllib

from .serializers import UploadFileSerializer
from .tesorero import *
from .models import *

# Create your views here.

# PATH_TEMP ruta donde se guardaran los archivos de excel temporalmente
PATH_TEMP = os.path.join(os.path.dirname(__file__),"temp")

TABLE_NAME = {
    "EMISION": "TRIBUTO_EMISION",
    "ALTAS": "TRIBUTO_ALTA",
    "BAJAS": "TRIBUTO_BAJA",
    "RECAUDACION": "TRIBUTO_RECAUDACION",
    "BENEFICIOS": "TRIBUTO_BENEFICIO"
}

DTYPE_TRIBUTOS = {
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
                    'cuenta-contable': str}
                   

}

RENAME_COLUMNS = {
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
        n_pc = request.META.get("COMPUTERNAME")

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
        n_pc = request.META.get("COMPUTERNAME")

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

def getTributoSelectContrib(valor, anio):

    tributos = []

    saldo_inicial = TributoSaldoInicialSelectContrib(valor)

    if len(saldo_inicial) > 0:
        nombre_tipo_tributo = saldo_inicial[0]["N_TipOpe"]
        tributos.append({
            "tipo": nombre_tipo_tributo,
            "anio": 0,
            "mes": 0,
            "detalle": saldo_inicial,
            "prioridad": 1
        })

    emision = TributoEmisionSelectContrib(valor, anio)

    if len(emision) > 0:
        nombre_tipo_tributo = emision[0]["N_TipOpe"]

        tributos.append({
            "tipo": nombre_tipo_tributo,
            "anio": anio,
            "mes": 0,
            "detalle": emision,
            "prioridad": 2
        })

    altas = TributoAltaSelectContrib(valor, anio)
    
    if altas:
        nombre_tipo_tributo = altas[0]["N_TipOpe"]
        tributos_dict = {}

        for alta in altas:
            clave = (nombre_tipo_tributo, alta["M_Archivo_Mes"])
            if clave not in tributos_dict:
                tributos_dict[clave] = {
                    "tipo": nombre_tipo_tributo,
                    "anio": anio,
                    "mes": alta["M_Archivo_Mes"],
                    "detalle": [],
                    "prioridad": 3                    
                }
            tributos_dict[clave]["detalle"].append(alta)    

        tributos += list(tributos_dict.values())

    bajas = TributoBajaSelectContrib(valor, anio)

    if bajas:
        nombre_tipo_tributo = bajas[0]["N_TipOpe"]
        tributos_dict = {}

        for baja in bajas:
            clave = (nombre_tipo_tributo, baja["M_Archivo_Mes"])
            if clave not in tributos_dict:
                tributos_dict[clave] = {
                    "tipo": nombre_tipo_tributo,
                    "anio": anio,
                    "mes": baja["M_Archivo_Mes"],
                    "detalle": [],
                    "prioridad": 4
                }
            tributos_dict[clave]["detalle"].append(baja)    

        tributos += list(tributos_dict.values())

    recaudacion = TributoRecaudacionSelectContrib(valor, anio)

    if recaudacion:
        nombre_tipo_tributo = recaudacion[0]["N_TipOpe"]
        tributos_dict = {}

        for rec in recaudacion:
            clave = (nombre_tipo_tributo, rec["M_Archivo_Mes"])
            if clave not in tributos_dict:
                tributos_dict[clave] = {
                    "tipo": nombre_tipo_tributo,
                    "anio": anio,
                    "mes": rec["M_Archivo_Mes"],
                    "detalle": [],
                    "prioridad": 5
                }
            tributos_dict[clave]["detalle"].append(rec)    

        tributos += list(tributos_dict.values())

    beneficios = TributoBeneficioSelectContrib(valor, anio)

    if beneficios:
        nombre_tipo_tributo = beneficios[0]["N_TipOpe"]
        tributos_dict = {}

        for ben in beneficios:
            clave = (nombre_tipo_tributo, ben["M_Archivo_Mes"])
            if clave not in tributos_dict:
                tributos_dict[clave] = {
                    "tipo": nombre_tipo_tributo,
                    "anio": anio,
                    "mes": ben["M_Archivo_Mes"],
                    "detalle": [],
                    "prioridad": 6
                }
            tributos_dict[clave]["detalle"].append(ben)    

        tributos += list(tributos_dict.values())

    # ordenar tributos por mes y prioridad

    tributos = sorted(tributos, key=lambda x: (x["mes"], x["prioridad"]))

    return tributos


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

