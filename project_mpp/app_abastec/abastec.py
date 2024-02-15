from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def SelectAccesoDepenReque(anio, login, depen = None, filtro = None):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectAccesodepenReque %s, %s, %s, %s', [anio, login, depen, filtro])
        return dictfetchall(cursor)     

def SelectRequeSf_dep(anio, sf_dep, bie_ser_tipo, field = None, valor = None, libre = None, tipo_gasto = None):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectRequeSf_dep %s, %s, %s, %s, %s, %s, %s', [anio, sf_dep, bie_ser_tipo, field, valor, libre, tipo_gasto])
        return dictfetchall(cursor)      

def SelectRequeById(anio, numero, tipo):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectRequeById %s, %s, %s', [anio, numero, tipo])
        return dictfetchall(cursor)     
    
def SelectAniosDepenById(anio, cod_dep):
    with connection.cursor() as cursor:
        field = "CODIGO_EXACTO"
        cursor.execute('EXEC SIGA.dbo.SelectDependencia %s, %s, %s', [anio, field, cod_dep])
        return dictfetchall(cursor)     
    
    

