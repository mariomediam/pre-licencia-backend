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

def UpdateContribuyente(codCont, nombre, tipoContrib, codLugar, codCalle, direcNro, direcPiso, direcMzna, direcLote, direcDpto, direcAdic, fecRegistro, responsable, motivo, profesion, homonimia, codAntContrib, sexo, fecNacimiento, codInmueble):
     with connection.cursor() as cursor:
        sql = """  
        DECLARE @RC int           
        DECLARE @C001Cod_Cont char(11) = %s
        DECLARE @C001Nombre varchar(150) = %s
        DECLARE @C001Tip_Cont char(2) = %s
        DECLARE @C001Cod_Lug char(9) = %s
        DECLARE @C001Cod_Calle char(4) = %s
        DECLARE @C001Numero char(4) = %s
        DECLARE @C001Piso char(2) = %s
        DECLARE @C001Manzana char(4) = %s
        DECLARE @C001Lote char(4) = %s
        DECLARE @C001Dpto char(4) = %s
        DECLARE @C001Direc_Adic varchar(70) = %s
        DECLARE @F001Fec_Reg datetime = %s
        DECLARE @C001Responsable varchar(30) = %s
        DECLARE @C001Motivo varchar(800) = %s
        DECLARE @C001Profesion char(5) = %s
        DECLARE @C001Homonimia char(1) = %s
        DECLARE @C001Cod_Ant_Cont char(1) = %s
        DECLARE @C001Sexo char(1) = %s
        DECLARE @D001FecNac datetime = %s
        DECLARE @C001CondInmueble char(3) = %s        

        EXECUTE @RC = BDSIAT2.dbo.spmUpdate_Contribuyente
        @C001Cod_Cont
        ,@C001Nombre
        ,@C001Tip_Cont
        ,@C001Cod_Lug
        ,@C001Cod_Calle
        ,@C001Numero
        ,@C001Piso
        ,@C001Manzana
        ,@C001Lote
        ,@C001Dpto
        ,@C001Direc_Adic
        ,@F001Fec_Reg
        ,@C001Responsable
        ,@C001Motivo
        ,@C001Profesion
        ,@C001Homonimia
        ,@C001Cod_Ant_Cont
        ,@C001Sexo
        ,@D001FecNac
        ,@C001CondInmueble

        SELECT @RC AS rc
        """
        cursor.execute(sql, [codCont, nombre, tipoContrib, codLugar, codCalle, direcNro, direcPiso, direcMzna, direcLote, direcDpto, direcAdic, fecRegistro, responsable, motivo, profesion, homonimia, codAntContrib, sexo, fecNacimiento, codInmueble])

def DeleteDocumentoContrib(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM BDSIAT2.dbo.T002Doc_Cont WHERE C002Cod_Cont = %s', [codigo_contrib])
        

def EnviarDocumentoContrib(cod_cont, cadena_vb):
     with connection.cursor() as cursor:
        sql = """  
        DECLARE @RC int
        DECLARE @Cod_Cont char(11) = %s
        DECLARE @CadenaVb varchar(8000) = %s

        EXECUTE @RC = BDSIAT2.dbo.sp_Enviar_Doc_Cont
        @Cod_Cont
        ,@CadenaVb        
        """
        cursor.execute(sql, [cod_cont, cadena_vb])        

def DeleteTelefonoContrib(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM BDSIAT2.dbo.T008Telef_Cont WHERE C008Cod_Cont = %s', [codigo_contrib])


def EnviarTelefonoContrib(cod_cont, cadena_vb):
     with connection.cursor() as cursor:
        sql = """         
        DECLARE @RC int
        DECLARE @Cod_Cont char(11) = %s
        DECLARE @CadenaVb varchar(8000) = %s

        EXECUTE @RC = BDSIAT2.dbo.sp_Enviar_Tel_Cont
        @Cod_Cont
        ,@CadenaVb
        """
        cursor.execute(sql, [cod_cont, cadena_vb])

def DeleteDirElectContrib(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM BDSIAT2.dbo.T011Dir_Elect_Cont WHERE C011Cod_Cont = %s', [codigo_contrib])

def EnviarDirElectContrib(cod_cont, cadena_vb):
     with connection.cursor() as cursor:
        sql = """         
        DECLARE @RC int
        DECLARE @Cod_Cont char(11) = %s
        DECLARE @CadenaVb varchar(8000) =%s

        EXECUTE @RC = BDSIAT2.dbo.sp_Enviar_Dir_Cont 
        @Cod_Cont
        ,@CadenaVb
        """
        cursor.execute(sql, [cod_cont, cadena_vb])        


def DeleteNacionalidadContrib(codigo_contrib):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM BDSIAT2.dbo.T138ContNacion WHERE C138CodCont = %s', [codigo_contrib])

def EnviarNacionalidadContrib(cod_cont, cadena_vb):
     with connection.cursor() as cursor:
        sql = """         
        DECLARE @RC int
        DECLARE @Cod_Cont char(11) =%s
        DECLARE @CadenaVb varchar(8000) =%s

        EXECUTE @RC = BDSIAT2.dbo.sp_Enviar_Nac_Cont
        @Cod_Cont
        ,@CadenaVb        
        """
        cursor.execute(sql, [cod_cont, cadena_vb])            
