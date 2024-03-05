from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

def SelectAccesoDepenReque(anio, login, depen = None, filtro = None):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectAccesodepenReque %s, %s, %s, %s', [anio, login, depen, filtro])
        return dictfetchall(cursor)     

def SelectRequeSf_dep(anio, sf_dep, bie_ser_tipo, field = None, valor = None, libre = None, tipo_gasto = None):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectRequeSf_dep %s, %s, %s, %s, %s, %s, %s', [anio, sf_dep, bie_ser_tipo, field, valor, libre, tipo_gasto])
        return dictfetchall(cursor)      

def SelectRequeById(anio, numero, tipo):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectRequeById %s, %s, %s', [anio, numero, tipo])
        return dictfetchall(cursor)     
    
def SelectAniosDepenById(anio, cod_dep):
    with connection.cursor() as cursor:
        field = "CODIGO_EXACTO"
        cursor.execute('EXEC SIGA.dbo.SelectDependencia %s, %s, %s', [anio, field, cod_dep])
        return dictfetchall(cursor)     
    
def SelectSaldoPresupDepen(anio, cod_dep, bie_ser_tipo):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectSaldoPresupDepen %s, %s, %s', [anio, cod_dep, bie_ser_tipo])
        return dictfetchall(cursor)    

def SelectBBSSDisponibleOrden(anio, sec_fun, cod_dep, bie_ser_tipo, file, valor):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectBBSSDisponibleOrden %s, %s, %s, %s, %s, %s', [anio, sec_fun, cod_dep, bie_ser_tipo, file, valor])
        return dictfetchall(cursor)    

def InsertRequeMyXML(params):    
    anipre = params.get('anipre')
    numero = params.get('numero')
    fecha = params.get('fecha')
    obs = params.get('obs')
    tipogasto = params.get('tipogasto')
    biesertipo = params.get('biesertipo')
    sf_dep = params.get('sf_dep')
    my_xml = params.get('my_xml')
    user = params.get('user')
    libre = params.get('libre')
    depen = params.get('depen')
    traba_dni = params.get('traba_dni')
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.InsertRequeMyXML %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s', [anipre, numero, fecha, obs, tipogasto, biesertipo, sf_dep, my_xml, user, libre, depen, traba_dni])
        
        results = []
        do = True
        while do:
            row = dictfetchall(cursor)
            if row:
                results.append(row)
            do = cursor.nextset()  # Move to the next result set, if available
        return results