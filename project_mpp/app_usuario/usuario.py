from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def login(usuario, password, sistema='36'):
    with connection.cursor() as cursor:
        cursor.execute('EXEC GENERAL.dbo.S07ValidarUsuario2 %s, %s, %s', [usuario, password, sistema])
        return dictfetchall(cursor)        

def leerMenues(usuario, sistema, opcion=None):
    with connection.cursor() as cursor:
        cursor.execute('EXEC GENERAL.dbo.S07LeerMenues %s, %s, %s', [usuario, sistema, opcion])
        return dictfetchall(cursor)            

def leerUserMenues(usuario, sistema):
    with connection.cursor() as cursor:
        cursor.execute('EXEC GENERAL.dbo.S07LeerUserMenues %s, %s', [usuario, sistema])
        return dictfetchall(cursor)        


