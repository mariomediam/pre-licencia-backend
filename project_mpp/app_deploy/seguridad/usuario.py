from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def login(usuario, password, sistema='02'):
    with connection.cursor() as cursor:        
        cursor.execute('EXEC GENERAL.dbo.S07ValidarUsuario2 %s, %s, %s', [usuario, password, sistema])        
        return dictfetchall(cursor)    

def get_user_by_login(login):
    with connection.cursor() as cursor:
        cursor.execute('EXEC GENERAL.dbo.S07BuscarUsuario %s, %s', ['C', login])
        result = dictfetchall(cursor)
        if len(result) > 0:
            return result[0]
        else:
            return None

