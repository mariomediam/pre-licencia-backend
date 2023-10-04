import string
from django.db import connection
from app_deploy.general.ejecutar import dictfetchall, namedtuplefetchall

def SelectPlan_estrategico(campo, valor):
    with connection.cursor() as cursor:
        cursor.execute('EXEC SIGA.dbo.SelectPlan_estrategico %s, %s', [valor, campo])
        return dictfetchall(cursor)  

def InsertPlan_estrategico(n_planest_desc, user):
    with connection.cursor() as cursor:
        sql = """
        SET NOCOUNT ON;
        EXEC SIGA.dbo.InsertPlanEst %s, %s;
        """

        cursor.execute(sql, [n_planest_desc, user])

def UpdatePlan_estrategico(n_planest_desc, c_planest, f_planest_activo, user):
    with connection.cursor() as cursor:
        sql = """
        SET NOCOUNT ON;
        EXEC SIGA.dbo.UpdatePlanEst %s, %s; %s; %s;
        """
        cursor.execute(sql, [n_planest_desc, c_planest, f_planest_activo, user])


def DeletePlan_estrategico(c_planest, f_planest_activo, user):
    with connection.cursor() as cursor:
        sql = """
        SET NOCOUNT ON;
        EXEC SIGA.dbo.DeletePlanEst %s, %s; %s;
        """
        cursor.execute(sql, [c_planest, f_planest_activo, user])
