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
        

def TributoPeriodosDisponibles(C_TipOpe, M_Archivo_Anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoPeriodosDisponibles %s, %s;
        """
        cursor.execute(sql, [C_TipOpe, M_Archivo_Anio])        
        return dictfetchall(cursor)

def TributoSaldoInicialSelectContrib(Valor, anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoSaldoInicialSelectContrib %s, %s;
        """
        cursor.execute(sql, [Valor, anio])        
        return dictfetchall(cursor)

def TributoEmisionSelectContrib(Valor, anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoEmisionSelectContrib %s, %s;
        """
        cursor.execute(sql, [Valor, anio])        
        return dictfetchall(cursor)
    
def TributoAltaSelectContrib(Valor, anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoAltaSelectContrib %s, %s;
        """
        cursor.execute(sql, [Valor, anio])        
        return dictfetchall(cursor)
    
def TributoBajaSelectContrib(Valor, anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoBajaSelectContrib %s, %s;
        """
        cursor.execute(sql, [Valor, anio])        
        return dictfetchall(cursor)
    
def TributoRecaudacionSelectContrib(Valor, anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoRecaudacionSelectContrib %s, %s;
        """
        cursor.execute(sql, [Valor, anio])        
        return dictfetchall(cursor)
    
def TributoBeneficioSelectContrib(Valor, anio):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoBeneficioSelectContrib %s, %s;
        """
        cursor.execute(sql, [Valor, anio])        
        return dictfetchall(cursor)

def TributoOpeFinDelete(C_OpeFin, C_Archivo, C_Usuari_Login, N_PC):
    with connection.cursor() as cursor:
        sql = """           
        EXEC SIGA.dbo.TributoOpeFinDelete %s, %s, %s, %s;
        """
        cursor.execute(sql, [C_OpeFin, C_Archivo, C_Usuari_Login, N_PC]) 


def TributoSaldoInicialInsert(C_Archivo, C_SalIni_Contrib, N_SalIni_Contrib, M_SalIni_Anio, Q_SalIni_Monto, C_SalIni_Partida, N_SalIni_Partida, C_SalIni_CtaCon, C_Usuari_Login, N_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        declare @C_OpeFin int

        EXEC SIGA.dbo.TributoSaldoInicialInsert %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @C_OpeFin OUTPUT;

        SELECT @C_OpeFin as C_OpeFin;
        """
        cursor.execute(sql, [C_Archivo, C_SalIni_Contrib, N_SalIni_Contrib, M_SalIni_Anio, Q_SalIni_Monto, C_SalIni_Partida, N_SalIni_Partida, C_SalIni_CtaCon, C_Usuari_Login, N_PC])   
        result = dictfetchall(cursor)

        if len(result) > 0:
            result = result[0]
        else:   
            result = None
        
        return result
    

def TributoEmisionInsert(C_Archivo, C_Emision_Contrib, N_Emision_Contrib, C_Emision_Partida, N_Emision_Partida, Q_Emision_Monto, C_Emision_CtaCon, C_Usuari_Login, N_Emision_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        declare @C_OpeFin int

        EXEC SIGA.dbo.TributoEmisionInsert %s, %s, %s, %s, %s, %s, %s, %s, %s, @C_OpeFin OUTPUT;

        SELECT @C_OpeFin as C_OpeFin;
        """
        cursor.execute(sql, [C_Archivo, C_Emision_Contrib, N_Emision_Contrib, C_Emision_Partida, N_Emision_Partida, Q_Emision_Monto, C_Emision_CtaCon, C_Usuari_Login, N_Emision_PC])   
        result = dictfetchall(cursor)

        if len(result) > 0:
            result = result[0]
        else:   
            result = None
        
        return result
    
def TributoAltaInsert(C_Archivo, D_Alta, C_Alta_Contrib, N_Alta_Contrib, M_Alta_Anio, C_Alta_Partida, N_Alta_Partida, Q_Alta_Monto, C_Alta_CtaCon, C_Usuari_Login, N_Alta_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        declare @C_OpeFin int

        EXEC SIGA.dbo.TributoAltaInsert %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @C_OpeFin OUTPUT;

        SELECT @C_OpeFin as C_OpeFin;
        """
        cursor.execute(sql, [C_Archivo, D_Alta, C_Alta_Contrib, N_Alta_Contrib, M_Alta_Anio, C_Alta_Partida, N_Alta_Partida, Q_Alta_Monto, C_Alta_CtaCon, C_Usuari_Login, N_Alta_PC])
        result = dictfetchall(cursor)

        if len(result) > 0:
            result = result[0]
        else:
            result = None

        return result

def TributoBajaInsert(C_Archivo, D_Baja, C_Baja_Contrib, N_Baja_Contrib, M_Baja_Anio, C_Baja_Partida, N_Baja_Partida, Q_Baja_Monto, C_Baja_CtaCon, C_Usuari_Login, N_Baja_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        declare @C_OpeFin int

        EXEC SIGA.dbo.TributoBajaInsert
        @C_Archivo = %s,
        @D_Baja = %s,
        @C_Baja_Contrib = %s,
        @N_Baja_Contrib = %s,
        @M_Baja_Anio = %s,
        @C_Baja_Partida = %s,
        @N_Baja_Partida = %s,
        @Q_Baja_Monto = %s,
        @C_Baja_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Baja_PC = %s,
        @C_OpeFin = @C_OpeFin OUTPUT;

        SELECT @C_OpeFin as C_OpeFin;
        """

        cursor.execute(sql, [C_Archivo, D_Baja, C_Baja_Contrib, N_Baja_Contrib, M_Baja_Anio, C_Baja_Partida, N_Baja_Partida, Q_Baja_Monto, C_Baja_CtaCon, C_Usuari_Login, N_Baja_PC])

        result = dictfetchall(cursor)

        if len(result) > 0:
            result = result[0]
        else:
            result = None

        return result
    
def TributoRecaudacionInsert(C_Archivo, D_Recaud, M_Recaud_Recibo, C_Recaud_Contrib, N_Recaud_Contrib, C_Recaud_Partida, N_Reacud_Partida, M_Recaud_Anio, Q_Recaud_Monto, C_Recaud_CtaCon, C_Usuari_Login, N_Recaud_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        declare @C_OpeFin int

        EXEC SIGA.dbo.TributoRecaudacionInsert
        @C_Archivo = %s,
        @D_Recaud = %s,
        @M_Recaud_Recibo = %s,
        @C_Recaud_Contrib = %s,
        @N_Recaud_Contrib = %s,
        @C_Recaud_Partida = %s,
        @N_Reacud_Partida = %s,
        @M_Recaud_Anio = %s,
        @Q_Recaud_Monto = %s,
        @C_Recaud_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Recaud_PC = %s,
        @C_OpeFin = @C_OpeFin OUTPUT;

        SELECT @C_OpeFin as C_OpeFin;
        """

        cursor.execute(sql, [C_Archivo, D_Recaud, M_Recaud_Recibo, C_Recaud_Contrib, N_Recaud_Contrib, C_Recaud_Partida, N_Reacud_Partida, M_Recaud_Anio, Q_Recaud_Monto, C_Recaud_CtaCon, C_Usuari_Login, N_Recaud_PC])

        result = dictfetchall(cursor)

        if len(result) > 0:
            result = result[0]
        else:
            result = None

        return result
    
def TributoBeneficioInsert(C_Archivo, C_Benefi_Contrib, N_Benefi_Contrib, M_Benefi_Recibo, M_Benefi_Anio, C_Benefi_Partida, N_Benefi_Partida, D_Benefi_Pago, N_Benefi_BasLeg, Q_Benefi_Monto, C_Benefi_CtaCon, C_Usuari_Login, N_Benefi_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        declare @C_OpeFin int

        EXEC SIGA.dbo.TributoBeneficioInsert
        @C_Archivo = %s,
        @C_Benefi_Contrib = %s,
        @N_Benefi_Contrib = %s,
        @M_Benefi_Recibo = %s,
        @M_Benefi_Anio = %s,
        @C_Benefi_Partida = %s,
        @N_Benefi_Partida = %s,
        @D_Benefi_Pago = %s,
        @N_Benefi_BasLeg = %s,
        @Q_Benefi_Monto = %s,
        @C_Benefi_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Benefi_PC = %s,
        @C_OpeFin = @C_OpeFin OUTPUT;

        SELECT @C_OpeFin as C_OpeFin;
        """

        cursor.execute(sql, [C_Archivo, C_Benefi_Contrib, N_Benefi_Contrib, M_Benefi_Recibo, M_Benefi_Anio, C_Benefi_Partida, N_Benefi_Partida, D_Benefi_Pago, N_Benefi_BasLeg, Q_Benefi_Monto, C_Benefi_CtaCon, C_Usuari_Login, N_Benefi_PC])

        result = dictfetchall(cursor)

        if len(result) > 0:
            result = result[0]
        else:
            result = None

        return result

def TributoSaldoInicialUpdate(C_OpeFin, C_SalIni_Contrib, N_SalIni_Contrib, M_SalIni_Anio, Q_SalIni_Monto, C_SalIni_Partida, N_SalIni_Partida, C_SalIni_CtaCon, C_Usuari_Login, N_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoSaldoInicialUpdate
        @C_OpeFin = %s,
        @C_SalIni_Contrib = %s,
        @N_SalIni_Contrib = %s,
        @M_SalIni_Anio = %s,
        @Q_SalIni_Monto = %s,
        @C_SalIni_Partida = %s,
        @N_SalIni_Partida = %s,
        @C_SalIni_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_SalIni_PC = %s;
        """
        cursor.execute(sql, [C_OpeFin, C_SalIni_Contrib, N_SalIni_Contrib, M_SalIni_Anio, Q_SalIni_Monto, C_SalIni_Partida, N_SalIni_Partida, C_SalIni_CtaCon, C_Usuari_Login, N_PC])

def TributoEmisionUpdate(C_OpeFin, C_Emision_Contrib, N_Emision_Contrib, C_Emision_Partida, N_Emision_Partida, Q_Emision_Monto, C_Emision_CtaCon, C_Usuari_Login, N_Emision_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoEmisionUpdate
        @C_OpeFin = %s,
        @C_Emision_Contrib = %s,
        @N_Emision_Contrib = %s,
        @C_Emision_Partida = %s,
        @N_Emision_Partida = %s,
        @Q_Emision_Monto = %s,
        @C_Emision_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Emision_PC = %s;
        """
        cursor.execute(sql, [C_OpeFin, C_Emision_Contrib, N_Emision_Contrib, C_Emision_Partida, N_Emision_Partida, Q_Emision_Monto, C_Emision_CtaCon, C_Usuari_Login, N_Emision_PC])


def TributoAltaUpdate(C_OpeFin, D_Alta, C_Alta_Contrib, N_Alta_Contrib, M_Alta_Anio, C_Alta_Partida, N_Alta_Partida, Q_Alta_Monto, C_Alta_CtaCon, C_Usuari_Login, N_Alta_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoAltaUpdate
        @C_OpeFin = %s,
        @D_Alta = %s,
        @C_Alta_Contrib = %s,
        @N_Alta_Contrib = %s,
        @M_Alta_Anio = %s,
        @C_Alta_Partida = %s,
        @N_Alta_Partida = %s,
        @Q_Alta_Monto = %s,
        @C_Alta_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Alta_PC = %s;
        """
        cursor.execute(sql, [C_OpeFin, D_Alta, C_Alta_Contrib, N_Alta_Contrib, M_Alta_Anio, C_Alta_Partida, N_Alta_Partida, Q_Alta_Monto, C_Alta_CtaCon, C_Usuari_Login, N_Alta_PC])


def TributoBajaUpdate(C_OpeFin, D_Baja, C_Baja_Contrib, N_Baja_Contrib, M_Baja_Anio, C_Baja_Partida, N_Baja_Partida, Q_Baja_Monto, C_Baja_CtaCon, C_Usuari_Login, N_Baja_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoBajaUpdate
        @C_OpeFin = %s,
        @D_Baja = %s,
        @C_Baja_Contrib = %s,
        @N_Baja_Contrib = %s,
        @M_Baja_Anio = %s,
        @C_Baja_Partida = %s,
        @N_Baja_Partida = %s,
        @Q_Baja_Monto = %s,
        @C_Baja_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Baja_PC = %s;
        """
        cursor.execute(sql, [C_OpeFin, D_Baja, C_Baja_Contrib, N_Baja_Contrib, M_Baja_Anio, C_Baja_Partida, N_Baja_Partida, Q_Baja_Monto, C_Baja_CtaCon, C_Usuari_Login, N_Baja_PC])


def TributoRecaudacionUpdate(C_OpeFin, D_Recaud, M_Recaud_Recibo, C_Recaud_Contrib, N_Recaud_Contrib, C_Recaud_Partida, N_Reacud_Partida, M_Recaud_Anio, Q_Recaud_Monto, C_Recaud_CtaCon, C_Usuari_Login, N_Recaud_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoRecaudacionUpdate
        @C_OpeFin = %s,
        @D_Recaud = %s,
        @M_Recaud_Recibo = %s,
        @C_Recaud_Contrib = %s,
        @N_Recaud_Contrib = %s,
        @C_Recaud_Partida = %s,
        @N_Reacud_Partida = %s,
        @M_Recaud_Anio = %s,
        @Q_Recaud_Monto = %s,
        @C_Recaud_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Recaud_PC = %s;
        """
        cursor.execute(sql, [C_OpeFin, D_Recaud, M_Recaud_Recibo, C_Recaud_Contrib, N_Recaud_Contrib, C_Recaud_Partida, N_Reacud_Partida, M_Recaud_Anio, Q_Recaud_Monto, C_Recaud_CtaCon, C_Usuari_Login, N_Recaud_PC])

def TributoBeneficioUpdate(C_OpeFin, C_Benefi_Contrib, N_Benefi_Contrib, M_Benefi_Recibo, M_Benefi_Anio, C_Benefi_Partida, N_Benefi_Partida, D_Benefi_Pago, N_Benefi_BasLeg, Q_Benefi_Monto, C_Benefi_CtaCon, C_Usuari_Login, N_Benefi_PC):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoBeneficioUpdate
        @C_OpeFin = %s,
        @C_Benefi_Contrib = %s,
        @N_Benefi_Contrib = %s,
        @M_Benefi_Recibo = %s,
        @M_Benefi_Anio = %s,
        @C_Benefi_Partida = %s,
        @N_Benefi_Partida = %s,
        @D_Benefi_Pago = %s,
        @N_Benefi_BasLeg = %s,
        @Q_Benefi_Monto = %s,
        @C_Benefi_CtaCon = %s,
        @C_Usuari_Login = %s,
        @N_Benefi_PC = %s;
        """
        cursor.execute(sql, [C_OpeFin, C_Benefi_Contrib, N_Benefi_Contrib, M_Benefi_Recibo, M_Benefi_Anio, C_Benefi_Partida, N_Benefi_Partida, D_Benefi_Pago, N_Benefi_BasLeg, Q_Benefi_Monto, C_Benefi_CtaCon, C_Usuari_Login, N_Benefi_PC])


def TributoOpeFinSelect(C_OpeFin, C_Archivo):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoOpeFinSelect
        @C_OpeFin = %s,
        @C_Archivo = %s;
        """
        cursor.execute(sql, [C_OpeFin, C_Archivo])        
        return dictfetchall(cursor) 

def TributoContibuyentePartida(M_Archivo_Anio, mes_hasta, contrib):
    with connection.cursor() as cursor:
        sql = """           
        SET NOCOUNT ON;
        EXEC SIGA.dbo.TributoContibuyentePartida
        @M_Archivo_Anio = %s,
        @mes_hasta = %s,
        @contrib = %s;
        """
        cursor.execute(sql, [M_Archivo_Anio, mes_hasta, contrib])        
        return dictfetchall(cursor)