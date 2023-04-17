import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def ListaPlanillaDetalle(anio, mes, tipo, numero, dni, n_user, c_banco_id):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.ListaPlanillaDetalle %s, %s, %s, %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero, dni, n_user, c_banco_id])        
        return dictfetchall(cursor)   
    

def SelectPlanillaBoleta(anio, mes):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.SelectPlanillaBoleta %s, %s;
        """
        cursor.execute(sql, [anio, mes])        
        return dictfetchall(cursor)   
    

