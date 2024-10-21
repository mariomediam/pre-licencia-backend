from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def sf_listar_maestro_documento():
    with connection.cursor() as cursor:
        sql = """           
        EXEC BDSIAF.dbo.sf_listar_maestro_documento;
        """
        cursor.execute(sql)        
        return dictfetchall(cursor)

def sf_seleccionar_persona(filtro):
    with connection.cursor() as cursor:
        sql = """           
        EXEC BDSIAF.dbo.sf_seleccionar_persona @filtro = %s;
        """
        cursor.execute(sql, [filtro])        
        return dictfetchall(cursor)
    

def sf_seleccionar_proveedor(filtro):
    with connection.cursor() as cursor:
        sql = """           
        EXEC BDSIAF.dbo.sf_seleccionar_proveedor @filtro = %s;
        """
        cursor.execute(sql, [filtro])        
        return dictfetchall(cursor)