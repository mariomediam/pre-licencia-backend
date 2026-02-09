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


def S42SincronizaRecaudacion(opcion, anio, valor):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SincronizaRecaudacion %s, %s, %s
        """
        cursor.execute(sql, [opcion, anio, valor])
        return dictfetchall(cursor)


def S42SelectRecaudacionPorAnioyDependencia(anio, dependencia):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SelectRecaudacionPorAnioyDependencia %s, %s
        """
        cursor.execute(sql, [anio, dependencia])
        return dictfetchall(cursor)


def S42SelectProyeccionPorAnioyDependencia(opcion, anio, dependencia):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SelectProyeccionPorAnioyDependencia %s, %s, %s
        """
        cursor.execute(sql, [opcion, anio, dependencia])
        return dictfetchall(cursor)


# CREATE PROCEDURE [dbo].[S42SelectRecaudacionPorAnioyTasa]
# @M_Recaud_Anio smallint,
# @C_Tasa int

def S42SelectRecaudacionPorAnioyTasa(anio, tasa):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SelectRecaudacionPorAnioyTasa %s, %s
        """
        cursor.execute(sql, [anio, tasa])
        return dictfetchall(cursor)

# ALTER PROCEDURE [dbo].[S42SelectProyeccionPorAnioyTasa]
# @C_Opcion char(2) = '01',
# @M_Proyecc_Anio smallint,
# @C_Tasa int


def S42SelectProyeccionPorAnioyTasa(opcion, anio, tasa):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SelectProyeccionPorAnioyTasa %s, %s, %s
        """
        cursor.execute(sql, [opcion, anio, tasa])
        return dictfetchall(cursor)


# CREATE PROCEDURE S42SelectTasa
# @opcion char(2),
# @valor varchar(max)

def S42SelectTasa(opcion, valor):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SelectTasa %s, %s
        """
        cursor.execute(sql, [opcion, valor])
        return dictfetchall(cursor)

# CREATE PROCEDURE S42UpdateTasa
# @C_Tasa int,
# @C_Depend int,
# @C_Usuari_Login char(20)

def S42UpdateTasa(tasa, dependencia, usuario):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42UpdateTasa %s, %s, %s
        """
        cursor.execute(sql, [tasa, dependencia, usuario])
        return True