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
