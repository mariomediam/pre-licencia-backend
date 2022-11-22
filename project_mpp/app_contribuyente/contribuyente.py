import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def BuscarContribNombre(nombre_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.sp001Contrib_Nombres %s', [nombre_contrib])
        return dictfetchall(cursor) 

def BuscarContribCodigo(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.sp001Contribuyente_Codigo %s', [codigo_contrib])
        return dictfetchall(cursor)         

def ConsultaContribCodigo(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spConsulta_Contribuyente_Codigo %s', [codigo_contrib])
        return dictfetchall(cursor)  

def ConsultaDocumentoNumero(numero_documento):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spConsulta_Codigo_Doc_Cont  %s', [numero_documento])
        return dictfetchall(cursor)          

def ListarTipoContribuyente():
    with connection.cursor() as cursor:
        cursor.execute('SELECT C004Tip_Cont,C004Nombre from BDSIAT2.dbo.T004TIP_CONT')
        return dictfetchall(cursor)    

def ConsultaTipoLugar():
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spmConsulta_Tip_Lug')
        return dictfetchall(cursor)

def ConsultaSectores():
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spmConsulta_Sectores')
        return dictfetchall(cursor)        

def ConsultaLugaresGeneral(codigo, nombre, tipo_lugar, sector, calificacion, dpto, prov, dist):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spmConsulta_Lugares_General %s, %s, %s, %s, %s, %s, %s, %s', [codigo, nombre, tipo_lugar, sector, calificacion, dpto, prov, dist])
        return dictfetchall(cursor)         

def ConsultaTipLugCodigo(codigo):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spmConsulta_Tip_Lug_Codigo %s', [codigo])
        return dictfetchall(cursor)                 