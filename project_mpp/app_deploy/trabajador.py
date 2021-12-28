from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def select_trabajador(field, valor_buscado):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAM.dbo.SelectTrabajador %s, %s', [field, valor_buscado])
        return dictfetchall(cursor)        