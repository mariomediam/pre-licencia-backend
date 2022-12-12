import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def BuscarContribNombre(nombre_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.sp001Contrib_Nombres %s', [nombre_contrib])
        # cursor.execute('EXEC BDSIAT2.dbo.sp001Contrib_Nombres {}'.format(nombre_contrib))
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
    
def ConsultaTelefonoCont(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spConsulta_Telef_Cont %s', [codigo_contrib])
        return dictfetchall(cursor)    

def ConsultaDocumentoCont(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spConsulta_Doc_Cont %s', [codigo_contrib])
        return dictfetchall(cursor)        
    
def ConsultaDirElectCont(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spConsulta_Dir_Elect_Cont %s', [codigo_contrib])
        return dictfetchall(cursor)                

def ConsultaNacionalidadCont(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spConsulta_Nacionalidad_Cont %s', [codigo_contrib])
        return dictfetchall(cursor)            
    

def separaNombre(nombre):
    with connection.cursor() as cursor:                
        sql = """\
        DECLARE @apellido1 varchar(70), @apellido2 varchar(70), @nombre1 varchar(70)

        EXEC BDSIAT2.dbo.spSepara_Nombre %s, @apellido1 = @apellido1 OUTPUT, @apellido2 = @apellido2 OUTPUT, @nombre1 = @nombre1 OUTPUT;

        SELECT @apellido1 as separa_pepat, @apellido2 as separa_apemat, @nombre1 as separa_nombre;
        """

        cursor.execute(sql, [nombre])
        return dictfetchall(cursor)[0]    


def ConsultaCallesGeneral(codigo, nombre):
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spmConsulta_Calles_General %s, %s', [codigo, nombre])
        return dictfetchall(cursor)        


def ListarTipDoc():
    with connection.cursor() as cursor:
        cursor.execute('SELECT C003Cod_Doc, C003Nombre, C003Especificacion, I003Longitud, F003Fecha, C003Responsable, C003Motivo, C003Infocorp FROM BDSIAT2.dbo.T003Tip_Doc')
        return dictfetchall(cursor)          


def ConsultaDocumentoTipoNro(codigo_docum, numero_docum):
    with connection.cursor() as cursor:
        sql = """     
        DECLARE @C002Cod_Doc char(2), @C002Num_Doc char(11)

        select @C002Cod_Doc = %s, @C002Num_Doc = %s

        SELECT T002Doc_Cont.C002Cod_Cont,
        T001Contribuyente.C001Nombre,
        T002Doc_Cont.C002Cod_Doc,
        T002Doc_Cont.C002Num_Doc 
        FROM BDSIAT2.dbo.T002Doc_Cont AS T002Doc_Cont
        INNER JOIN BDSIAT2.dbo.T001Contribuyente AS T001Contribuyente
        ON T002Doc_Cont.C002Cod_Cont = T001Contribuyente.C001Cod_Cont 
        WHERE T002Doc_Cont.C002Cod_Doc = @C002Cod_Doc 
        AND RTRIM(LTRIM(T002Doc_Cont.C002Num_Doc)) = RTRIM(LTRIM(@C002Num_Doc))
        """
        cursor.execute(sql, [codigo_docum, numero_docum])
        return dictfetchall(cursor)


def ConsultaTiposTelefono():
    with connection.cursor() as cursor:
        cursor.execute('EXEC BDSIAT2.dbo.spmConsultaTipos_Telefono')
        return dictfetchall(cursor)   


def ListarTipoNacion():
    with connection.cursor() as cursor:
        cursor.execute('SELECT C163CodNacion, C163Nombres, D163Fecha, C163Responsable, C163Gentilicio1, C163Gentilicio2 FROM BDSIAT2.dbo.T163Nacion ORDER BY C163Nombres')
        return dictfetchall(cursor)          
