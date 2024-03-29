import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def ListaPlanillaDetalle(anio, mes, tipo, numero, dni, n_user, c_banco_id):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.ListaPlanillaDetalle %s, %s, %s, %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero, dni, n_user, c_banco_id])        
        return dictfetchall(cursor)   
    

def SelectPlanillaBoleta(anio, mes, tipo = None, numero = None):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.SelectPlanillaBoleta %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero])        
        return dictfetchall(cursor)   
    

def ListaPlanillaResumen(anio, mes, tipo, numero):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.ListaPlanillaResumen %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero])        
        return dictfetchall(cursor)   
    
def ListaBoletaPagoWeb(anio, mes, tipo, numero):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.ListaBoletaPagoWeb %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero])
        return dictfetchall(cursor)
    

def InsertBoletaCarpeta(anio, mes, tipo, numero, estado, carpeta, usuario):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.InsertBoletaCarpeta %s, %s, %s, %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero, estado, carpeta, usuario])
        
    
def UpdateBoletaCarpeta(anio, mes, tipo, numero, estado, carpeta, usuario):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.UpdateBoletaCarpeta %s, %s, %s, %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero, estado, carpeta, usuario])
        
    
def DeleteBoletaCarpeta(anio, mes, tipo, numero, usuario):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.DeleteBoletaCarpeta %s, %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero, usuario])
        
def SelectPlanillaBoletaGenerado(anio, mes, tipo, numero):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.SelectPlanillaBoletaGenerado %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero])        
        return dictfetchall(cursor)          


def SelectPlanillaTrabajadorCorreo(anio, mes, tipo, numero):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.SelectPlanillaTrabajadorCorreo %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero])        
        return dictfetchall(cursor)                  
    
def SelectTipoPlanillaxTipo(tipo):
    with connection.cursor() as cursor:
        sql = """
        declare @Field varchar(30) = 'IDTIPOPLANILLA'
        declare @Value varchar(30) = %s 
        SET NOCOUNT ON;
        EXEC SIAM.dbo.SelectTipoPlanilla @Field, @Value;
        """
        cursor.execute(sql, [tipo])        
        return dictfetchall(cursor)          


def UpdateBoletaCarpetaEnvio(anio, mes, tipo, numero, envio, usuario):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.UpdateBoletaCarpetaEnvio %s, %s, %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero, envio, usuario])



def InsertBoletaEnvio(anio, mes, tipo, numero, dni, correo, usuario):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.InsertBoleta_envio %s, %s, %s, %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero, dni, correo, usuario])



def SelectBoletaEnvio(anio, mes, tipo, numero):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.SelectBoletaEnvio %s, %s, %s, %s;
        """
        cursor.execute(sql, [anio, mes, tipo, numero])        
        return dictfetchall(cursor)           
    

def SelectTrabajadorCorreo(valor):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.SelectTrabajadorCorreo %s;
        """
        cursor.execute(sql, [valor])        
        return dictfetchall(cursor)               
    

def InsertUpdateTrabajadorCorreo(dni, correo, usuario):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.InsertUpdateTrabajadorCorreo %s, %s, %s;
        """
        cursor.execute(sql, [dni, correo, usuario])    


def DeleteTrabajadorCorreo(dni, usuario):
    with connection.cursor() as cursor:
        sql = """   
        SET NOCOUNT ON;
        EXEC SIAM.dbo.DeleteTrabajador_correo %s, %s;
        """
        cursor.execute(sql, [dni, usuario])                    

