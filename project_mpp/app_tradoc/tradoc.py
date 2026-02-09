import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall


def SeleccReqTupa(tiptra, tiptra_anio, tiptra_origen, reqtup_item, ocultar_recpag):
    with connection.cursor() as cursor:        
        cursor.execute('EXEC SIAC.dbo.S01SeleccReqTupa %s, %s, %s, %s, %s', [tiptra, tiptra_anio, tiptra_origen, reqtup_item, ocultar_recpag])        
        return dictfetchall(cursor) 

def SeleccDocumXNumero(c_depend, m_docum_numdoc, desde, hasta):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S17SeleccDocumXNumero %s, %s, %s, %s', [c_depend, m_docum_numdoc, desde, hasta])
        return dictfetchall(cursor)

def SeleccDocInterno(c_docum):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S17SeleccDocInterno %s', [c_docum])
        return dictfetchall(cursor)

def VerArbol(c_docum):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S17VerArbol %s', [c_docum])
        return dictfetchall(cursor)

def s17SelectDependencia(ano, field, valor, solo_activas):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.s17SelectDependencia %s, %s, %s, %s', [ano, field, valor, solo_activas])
        return dictfetchall(cursor)

