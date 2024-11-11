from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def sf_listar_maestro_documento():
    with connection.cursor() as cursor:
        sql = """           
        EXEC BDSIAF.dbo.sf_listar_maestro_documento;
        """
        cursor.execute(sql)        
        return dictfetchall(cursor)

def sf_seleccionar_persona(filtro):
    with connection.cursor() as cursor:
        sql = """           
        EXEC BDSIAF.dbo.sf_seleccionar_persona @filtro = %s;
        """
        cursor.execute(sql, [filtro])        
        return dictfetchall(cursor)
    

def sf_seleccionar_proveedor(filtro):
    with connection.cursor() as cursor:
        sql = """           
        EXEC BDSIAF.dbo.sf_seleccionar_proveedor @filtro = %s;
        """
        cursor.execute(sql, [filtro])        
        return dictfetchall(cursor)


def sf_seleccionar_registros(**kwargs):

    fecha1 = kwargs.get('fecha1', None)
    fecha2 = kwargs.get('fecha2', None)
    expediente = kwargs.get('expediente', None)
    ciclo = kwargs.get('ciclo', None)
    fase = kwargs.get('fase', None)
    rubro = kwargs.get('rubro', None)
    tipo_recurso = kwargs.get('tipo_recurso', None)
    meta = kwargs.get('meta', None)
    tipo_operacion = kwargs.get('tipo_operacion', None)
    cod_doc = kwargs.get('cod_doc', None)
    num_doc = kwargs.get('num_doc', None)
    glosa = kwargs.get('glosa', None)
    clasificador = kwargs.get('clasificador', None)
    certificado = kwargs.get('certificado', None)
    proveedor = kwargs.get('proveedor', None)
    ctacte = kwargs.get('ctacte', None)

    with connection.cursor() as cursor:
        sql = """           
        EXEC BDSIAF.dbo.sf_seleccionar_registros
        @fecha1 = %s,
        @fecha2 = %s,
        @expediente = %s,
        @ciclo = %s,
        @fase = %s,
        @rubro = %s,
        @tipo_recurso = %s,
        @meta = %s,
        @tipo_operacion = %s,
        @cod_doc = %s,
        @num_doc = %s,
        @glosa = %s,
        @clasificador = %s,
        @certificado = %s,
        @proveedor = %s,
        @ctacte = %s;
        """
        
        cursor.execute(sql, [fecha1, fecha2, expediente, ciclo, fase, rubro, tipo_recurso, meta, tipo_operacion, cod_doc, num_doc, glosa, clasificador, certificado, proveedor, ctacte])        
        return dictfetchall(cursor)