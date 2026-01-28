from django.db import connections
from app_deploy.general.ejecutar import dictfetchall


def BuscarRecaudacionSATP(anio, mes, tasas):
    with connections['BDSATP'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        

        exec BDSIAT2.DBO.sp_ver_Pagos_TASA_MPP_MMCHT %s, %s, %s
        """
        cursor.execute(sql, [anio, mes, tasas])
        return dictfetchall(cursor)


# ALTER PROCEDURE [dbo].[S42SincronizaRecaudacion]
# @Opcion char(2),
# @Anio char(4),
# @Valor varchar(max)
# AS

def S42SincronizaRecaudacion(opcion, anio, valor):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SincronizaRecaudacion %s, %s, %s
        """
        cursor.execute(sql, [opcion, anio, valor])
        return dictfetchall(cursor)
