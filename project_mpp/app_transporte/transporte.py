from django.db import connection
from app_deploy.general.ejecutar import dictfetchall


def S09TranspVigente():
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S09TranspVigente")
        return dictfetchall(cursor) 

def S09ComparaTranspxAnio(m_dia, m_mes, c_anio01, c_anio02, opcion = 1):
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S09ComparaTranspxAnio @m_dia = %s, @m_mes = %s, @c_anio01 = %s, @c_anio02 = %s, @opcion = %s", [m_dia, m_mes, c_anio01, c_anio02, opcion])        
        result = dictfetchall(cursor)
        if opcion == 1 and len(result) > 0:            
            return result[0]
        
        return result

def S09TranspxAnio(c_anio):
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S09TranspxAnio @c_anio = %s", [c_anio])
        return dictfetchall(cursor)

def S09TranspxAnioyMes(c_anio):
    with connection.cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        exec SIAC.dbo.S09TranspxAnioyMes @c_anio = %s
        """
        cursor.execute(sql, [c_anio])
        return dictfetchall(cursor)

def S05InfraccionesTransportexAnio(c_anio):
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S05InfraccionesTransportexAnio @c_anio = %s", [c_anio])
        return dictfetchall(cursor)

def S05ComparaInfraccTransportexAnio(m_dia, m_mes, c_anio01, c_anio02):
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S05ComparaInfraccTransportexAnio @m_dia = %s, @m_mes = %s, @c_anio01 = %s, @c_anio02 = %s", [m_dia, m_mes, c_anio01, c_anio02])
        result = dictfetchall(cursor)
        if len(result) > 0:
            return result[0]
        
        return result
    
def S09TranspAntigVehic():
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S09TranspAntigVehic")
        return dictfetchall(cursor)
    