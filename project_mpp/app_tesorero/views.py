import os
from django.shortcuts import render
from django.db import transaction
from datetime import datetime

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

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
    "EMISION": "TRIBUTO_EMISION"
}

DTYPE_TRIBUTOS = {
    "EMISION": {'cod-contribuyente': str, 
                'nombre-contribuyente': str,
                'cod-partida': str, 
                'nombre-partida': str,
                'importe': float, 
                'cuenta-contable': str}
}

RENAME_COLUMNS = {
    "EMISION": {'cod-contribuyente': 'C_Emision_Contrib',
                'nombre-contribuyente': 'N_Emision_Contrib',
                'cod-partida': 'C_Emision_Partida',
                'nombre-partida': 'N_Emision_Partida',
                'importe': 'Q_Emision_Monto',
                'cuenta-contable': 'C_Emision_CtaCon'}
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
    
    return df