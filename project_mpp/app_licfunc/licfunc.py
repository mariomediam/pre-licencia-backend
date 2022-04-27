import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall

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