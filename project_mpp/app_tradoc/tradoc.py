import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall


def SeleccReqTupa(tiptra, tiptra_anio, tiptra_origen, reqtup_item, ocultar_recpag):
    with connection.cursor() as cursor:        
        cursor.execute('EXEC SIAC.dbo.S01SeleccReqTupa %s, %s, %s, %s, %s', [tiptra, tiptra_anio, tiptra_origen, reqtup_item, ocultar_recpag])        
        return dictfetchall(cursor) 