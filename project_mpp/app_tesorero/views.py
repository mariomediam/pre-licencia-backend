import os
from django.shortcuts import render

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

import pandas as pd
from sqlalchemy import create_engine
import urllib

from .serializers import UploadFileSerializer


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
    "EMISION": {'cod-contribuyente': 'C_Contrib',
                'nombre-contribuyente': 'N_Contrib',
                'cod-partida': 'C_Partida',
                'nombre-partida': 'N_Partida',
                'importe': 'Q_Importe',
                'cuenta-contable': 'C_CtaCon'}
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
    df.insert(0, "C_anipre", "2024")

    # Inserta los datos en la tabla
    num_records = df.to_sql(name=nombre_tabla, 
              con=engine, 
              if_exists='append', 
              index=False)

    # Cierra la conexión
    engine.dispose()

    return num_records
