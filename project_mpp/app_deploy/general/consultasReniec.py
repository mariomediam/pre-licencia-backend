from django.db import connection
from app_deploy.general.ejecutar import dictfetchall, namedtuplefetchall


def AgregarConsultaReniec(c_usuari_login, m_dni, coResultado, apPrimer, apSegundo, direccion, estadoCivil, foto, prenombres, restriccion, ubigeo, deResultado):
     
     with connection.cursor() as cursor:
        sql = """  
        DECLARE @RC int
        DECLARE @c_usuari_login char(20) = %s
        DECLARE @m_dni char(20) = %s
        DECLARE @coResultado char(4) = %s
        DECLARE @apPrimer varchar(100) = %s
        DECLARE @apSegundo varchar(100) = %s
        DECLARE @direccion varchar(100) = %s
        DECLARE @estadoCivil varchar(100) = %s
        DECLARE @foto varchar(max) = %s
        DECLARE @prenombres varchar(100) = %s
        DECLARE @restriccion varchar(100) = %s
        DECLARE @ubigeo varchar(100) = %s
        DECLARE @deResultado varchar(100) = %s

        EXECUTE @RC = GENERAL.[dbo].[S07AgregarConsultasReniec] 
        @c_usuari_login
        ,@m_dni
        ,@coResultado
        ,@apPrimer
        ,@apSegundo
        ,@direccion
        ,@estadoCivil
        ,@foto
        ,@prenombres
        ,@restriccion
        ,@ubigeo
        ,@deResultado
        """
        
        cursor.execute(sql, [c_usuari_login, m_dni, coResultado, apPrimer, apSegundo, direccion, estadoCivil, foto, prenombres, restriccion, ubigeo, deResultado])


def ValidaAccesoConsultaReniec(c_usuari_login):
     
     with connection.cursor() as cursor:
        sql = """  
        DECLARE @RC int
        DECLARE @c_usuari_login char(20) = %s
        DECLARE @acceso bit

        EXECUTE @RC = GENERAL.[dbo].[S07ValidaAccesoConsultaReniec] 
        @c_usuari_login
        ,@acceso OUTPUT

        SELECT @acceso AS acceso
        """
        
        cursor.execute(sql, [c_usuari_login]) 
        return dictfetchall(cursor)[0]    