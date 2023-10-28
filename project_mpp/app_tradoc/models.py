from django.db import models

# Create your models here.


class ExpedientesModel(models.Model):

    ExpedId = models.CharField(max_length=8, null=False, db_column='C_Exped', primary_key=True)
    ExpedAnio = models.CharField(max_length=4, null=False, db_column='C_Exped_Anio')
    ExpedNumForm = models.CharField(max_length=8, null=False, db_column='M_Exped_NumForm')
    ExpedNumFol = models.CharField(max_length=4, null=False, db_column='Q_Exped_NumFol')
    ExpedFecIng = models.DateTimeField(null=False, db_column='D_Exped_FecIng')
    ExpedGlosa = models.CharField(max_length=200, null=False, db_column='T_Exped_Glosa')
    ExpedNumDoc = models.CharField(max_length=40, null=False, db_column='M_Exped_NumDoc')
    ExpedSolici = models.CharField(max_length=11, null=False, db_column='C_Exped_Solici')
    ExpedOrigen = models.CharField(max_length=1, null=False, db_column='F_TipTra_Origen')
    ExpedTipTra = models.CharField(max_length=8, null=False, db_column='C_TipTra')
    ExpedTipTraAnio = models.CharField(max_length=4, null=False, db_column='C_TipTra_Anio')
    ExpedTipDoc = models.CharField(max_length=2, null=True, db_column='C_TipDoc')
    ExpedRepLeg = models.CharField(max_length=11, null=True, db_column='C_Exped_RepLeg')
    ExpedObserv = models.CharField(max_length=500, null=True, db_column='C_Exped_Observ')
    ExpedArchProv = models.CharField(max_length=1, null=True, db_column='F_Exped_ArchProv')
    ExpedUsuariLogin = models.CharField(max_length=20, null=False, db_column='C_Usuari_Login')
    ExpedFecDig = models.DateTimeField(null=False, db_column='D_Exped_FecDig', auto_now=True)
    ExpedFinTramite = models.CharField(max_length=1, null=True, db_column='F_Exped_FinTramite')
    ExpedFecFinTram = models.DateTimeField(null=True, db_column='D_Exped_FecFinTram')
    ExpedTipDocFinal = models.CharField(max_length=2, null=True, db_column='C_TipDoc_Final')
    ExpedNumDocFinal = models.CharField(max_length=64, null=True, db_column='M_Exped_Final')
    ExpedGlosaFinal = models.CharField(max_length=200, null=True, db_column='T_Exped_Final')
    ExpedUsuariFinal = models.CharField(max_length=20, null=True, db_column='C_Usuari_Final')
    ExpedCiudAten = models.CharField(max_length=1, null=True, db_column='F_Exped_CiudAten')
    ExpedFecCiuAten = models.DateTimeField(null=True, db_column='D_Exped_FecCiuAten')

    class Meta:
        db_table = 'S17Expedientes'
        managed = False        
        unique_together = (('ExpedId', 'ExpedAnio'),) 