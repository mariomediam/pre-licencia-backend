import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def TributoSelect(C_TipOpe = None):
    with connection.cursor() as cursor:
        sql = """           
        EXEC SIGA.dbo.TributoSelect %s;
        """
        cursor.execute(sql, [C_TipOpe])        
        return dictfetchall(cursor)   


def TributoArchivoSelect(Opcion, Valor01 = None, Valor02 = None, Valor03 = None):
    with connection.cursor() as cursor:
        sql = """           
        EXEC SIGA.dbo.TributoArchivoSelect %s, %s, %s, %s;
        """
        cursor.execute(sql, [Opcion, Valor01, Valor02, Valor03])        
        return dictfetchall(cursor)

def TributoInsertArchivo(C_TipOpe, M_Archivo_Anio, M_Archivo_Mes, C_Usuari_Login, N_Archivo_PC):
    with connection.cursor() as cursor:
        sql = """         
        SET NOCOUNT ON;  
        declare @C_TipOpe char(2),
            @M_Archivo_Anio int,
            @M_Archivo_Mes int,
            @C_Usuari_Login char(20),
            @N_Archivo_PC varchar(20),
            @C_Archivo int

        EXEC SIGA.dbo.TributoInsertArchivo %s, %s, %s, %s, %s, @C_Archivo OUTPUT;

        SELECT @C_Archivo as C_Archivo;
        """
        cursor.execute(sql, [C_TipOpe, M_Archivo_Anio, M_Archivo_Mes, C_Usuari_Login, N_Archivo_PC])   
        result = dictfetchall(cursor)

        if len(result) > 0:
            result = result[0]
        else:   
            result = None
        
        return result
    
def TributoDeleteArchivo(C_Archivo, C_Usuari_Login, N_PC):
    with connection.cursor() as cursor:
        sql = """                
        EXEC SIGA.dbo.TributoDeleteArchivo %s, %s, %s;
        """
        cursor.execute(sql, [C_Archivo, C_Usuari_Login, N_PC])   
        
# go
# ALTER PROCEDURE TributoPeriodosDisponibles
# @C_TipOpe char(2),
# @M_Archivo_Anio int


def TributoPeriodosDisponibles(C_TipOpe, M_Archivo_Anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoPeriodosDisponibles %s, %s;
        """
        cursor.execute(sql, [C_TipOpe, M_Archivo_Anio])        
        return dictfetchall(cursor)