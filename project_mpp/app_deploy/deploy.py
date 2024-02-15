from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def SelectJefeDepen(anio, depen ):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectJefeDepen %s, %s', [anio, depen])
        return dictfetchall(cursor)     

