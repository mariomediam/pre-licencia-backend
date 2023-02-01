import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

tipo_funciones ={"1":"COMERCIO", "2":"ENCUENTRO", "3":"HOSPEDAJE", "4":"INDUSTRIAL", "5":"OFICINAS ADMINISTRATIVAS", "6":"SALUD"}

def TipoTramitePorLicencia(motivo_sol, tipo_sol, nivel_riesgo, area):
    with connection.cursor() as cursor:                
        sql = """\
        DECLARE @C_TipTra char(8), @F_TipTra_Origen char(1), @C_TipTra_Anio char(4);

        EXEC S17TipoTramitePorLicencia %s, %s, %s, %s, @C_TipTra = @C_TipTra OUTPUT, @F_TipTra_Origen = @F_TipTra_Origen OUTPUT, @C_TipTra_Anio = @C_TipTra_Anio OUTPUT;

        SELECT @C_TipTra as C_TipTra, @F_TipTra_Origen as F_TipTra_Origen, @C_TipTra_Anio as C_TipTra_Anio;
        """

        cursor.execute(sql, (motivo_sol, tipo_sol, nivel_riesgo, area))
        return dictfetchall(cursor)[0]


def BuscarRequisitoArchivo(opcion, valor01):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S17Web_LIC_BuscarRequisitoArchivo %s, %s', [opcion, valor01])
        return dictfetchall(cursor)        

def BuscarLicencGen(c_solici):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S02SeleccionarLicencGen %s', [c_solici])
        return dictfetchall(cursor)  


def ListarFunciones(funciones: string):
    array_funciones = []    
    for i in funciones:        
        nombre_funcion = tipo_funciones.get(i)
        if nombre_funcion is not None:
            dict_funciones = {'idFuncion': int(i), 'nombreFuncion': nombre_funcion}
            array_funciones.append(dict_funciones)
            

    return array_funciones

def BuscarDatosTrabajador(c_usuari_login):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S17WEB_Lic_SelectDatosTrab %s', [c_usuari_login])
        return dictfetchall(cursor)

def BuscarTipoTramite(c_tiptra, c_tiptra_anio, f_tiptra_origen):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S01SeleccTipoTramite %s, %s, %s', [c_tiptra, c_tiptra_anio, f_tiptra_origen])
        return dictfetchall(cursor)  

def ImprimirLicencia(c_licenc, f_licencia_origen):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S02ImprimirLicencia %s, %s', [c_licenc, f_licencia_origen])
        return dictfetchall(cursor)          

def BuscarGiroNegocio(area, xml_giros, area_mayor30):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S02BuscarGiroNegocio %s, %s, %s', [area, xml_giros, area_mayor30])
        return dictfetchall(cursor)          

def AgregarSol_GiroNegCiiu(c_solici, C_GiroNeg, c_usuari_login):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S02AgregarSol_GiroNegCiiu %s, %s, %s', [c_solici, C_GiroNeg, c_usuari_login])

def SeleccionarSolicitud(c_solici):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIAC.dbo.S02SeleccionarSolicitud %s', [c_solici])
        return dictfetchall(cursor)     

