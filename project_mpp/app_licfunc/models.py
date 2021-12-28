from django.db import models

# Create your models here.
class PrecalificacionModel(models.Model):

    precalId = models.AutoField(
        primary_key=True, null=False, db_column='idPreCalificacion', unique=True)

    precalContribCod = models.CharField(
        max_length=11, db_column='fkContribuyente', null=False)

    precalCodCatast = models.CharField(
        max_length=11, db_column='codigoCatastral', null=False)

    precalDireccion = models.CharField(
        max_length=300, db_column='direccionCatastral', null=False)

    precalArea = models.DecimalField(
        db_column='areaNegocio', max_digits=18, decimal_places=4, null=False)

    precalRiesgo = models.IntegerField(
        db_column='fkRiesgo', null=False, default=0)

    precalRiesgoEval = models.IntegerField(
        db_column='fkRiesgoEvaluado', null=False, default=0)

    precalFuncion = models.IntegerField(
        db_column='fkFuncion', null=False, default=0)

    precalCompatCU = models.IntegerField(
        db_column='fkCompatibilidadCU', null=False, default=0)

    precalCompatDL = models.IntegerField(
        db_column='fkCompatibilidadDL', null=False, default=0)

    precalMonto = models.DecimalField(
        db_column='monto', max_digits=12, decimal_places=2, null=False)

    precalEstado = models.CharField(
        max_length=1, db_column='estado', null=False)       

    precalObserv = models.TextField(db_column='observacion', null=True)

    precalDigitFecha = models.DateTimeField(auto_now=True, db_column='RecordCreateDate')

    precalDigitUser = models.CharField(
        max_length=100, db_column='RecordCreateUser', null=False)

    precalRecordEstado = models.CharField(
        max_length=1, db_column='RecordState', null=False)

    precalCompatDL = models.IntegerField(
        db_column='fkCompatibilidadDL', null=False, default=0)

    precalSolicitanteId = models.IntegerField(
        db_column='idContribuyente', null=False, default=0)

    precalDescripcion = models.TextField(db_column='descripcion', null=True)        

    def __str__(self):
        return str(self.precalId)

    class Meta:
        db_table = 'S17Web_LIC_PreCalificacion'


class TipoEvalModel(models.Model):
    tipoEvalId = models.AutoField(
        primary_key=True, null=False, db_column='C_TipEval', unique=True)

    tipoEvalNombre = models.CharField(
        max_length=50, db_column='N_TipEval', null=False)

    class Meta:
        db_table = 'S17Web_LIC_TipoEval'

class EvalUsuModel(models.Model):
    evalUsulId = models.AutoField(
        primary_key=True, null=False, db_column='C_EvalUsu', unique=True)

    tipoEval = models.ForeignKey(
        to=TipoEvalModel, related_name='evaluacionUsuarios', db_column='C_TipEval', on_delete=models.PROTECT)

    userLogin = models.CharField(
        max_length=20, db_column='C_Usuari_Login', null=False)

    class Meta:
        db_table = 'S17Web_LIC_EvalUsu'
        