from django.db import connection, connections
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

def S09OcurrenciasxAnio(c_opcion, c_anio):
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S09OcurrenciasxAnio @c_opcion = %s, @c_anio = %s", [c_opcion, c_anio])
        return dictfetchall(cursor)

def S09MontosPapeletaTransito(anio, tipo_infraccion, mes = None):
    with connection.cursor() as cursor:
        cursor.execute("exec SIAC.dbo.S09MontosPapeletaTransito @Annio = %s, @TipoInfraccion = %s, @Mes = %s", [anio, tipo_infraccion, mes])
        return dictfetchall(cursor)
    

def S05ComparaMontosPapeletaTransito(m_dia, m_mes, c_anio01, c_anio02):
    with connection.cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        exec SIAC.dbo.S05ComparaMontosPapeletaTransito @m_dia = %s, @m_mes = %s, @c_anio01 = %s, @c_anio02 = %s
        """

        cursor.execute(sql, [m_dia, m_mes, c_anio01, c_anio02])


        # cursor.execute("exec SIAC.dbo.S05ComparaMontosPapeletaTransito @m_dia = %s, @m_mes = %s, @c_anio01 = %s, @c_anio02 = %s", [m_dia, m_mes, c_anio01, c_anio02])
        result = dictfetchall(cursor)
        if len(result) > 0:
            return result[0]
        
        return result


def S42SelectCapacitacion(opcion, valor1 = None, valor2 = None):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SelectCapacitacion %s, %s, %s
        """
        cursor.execute(sql, [opcion, valor1, valor2])
        return dictfetchall(cursor)

def S42SelectCapacitacionObservacion(opcion, valor1 = None, valor2 = None):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42SelectCapacitacionObservacion %s, %s, %s
        """
        cursor.execute(sql, [opcion, valor1, valor2])
        return dictfetchall(cursor)

def S42InsertarCapacitacion(fecha, tema, modalidad, capacitador, empresas, lugar, cantidad, observacion, usuario):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42InsertarCapacitacion %s, %s, %s, %s, %s, %s, %s, %s, %s
        """
        cursor.execute(sql, [fecha, tema, modalidad, capacitador, empresas, lugar, cantidad, observacion, usuario])
        data = dictfetchall(cursor)
        if len(data) > 0:
            return data[0]
        
        return data


def S42UpdateCapacitacion(capacitacion, fecha, tema, modalidad, capacitador, empresas, lugar, cantidad, observacion, usuario):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42UpdateCapacitacion %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        """
        cursor.execute(sql, [capacitacion, fecha, tema, modalidad, capacitador, empresas, lugar, cantidad, observacion, usuario])
        return True

def S42DeleteCapacitacion(capacitacion, usuario):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42DeleteCapacitacion %s, %s
        """
        cursor.execute(sql, [capacitacion, usuario])
        return True


def S42InsertarCapacitacionObservacion(anio, mes, observacion, usuario):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42InsertarCapacitacionObservacion %s, %s, %s, %s
        """
        cursor.execute(sql, [anio, mes, observacion, usuario])
        data = dictfetchall(cursor)
        if len(data) > 0:
            return data[0]
        
        return data

# ALTER PROCEDURE [dbo].[S42UpdateCapacitacionObservacion]
# @C_Capacita_Observ int,
# @T_Capacita_Observ varchar(max),
# @C_Usuari_Login char(20)


def S42UpdateCapacitacionObservacion(id_observacion, observacion, usuario):
    with connections['default'].cursor() as cursor:
        sql = """
        SET NOCOUNT ON
        
        exec S42UpdateCapacitacionObservacion %s, %s, %s
        """
        cursor.execute(sql, [id_observacion, observacion, usuario])
        return True