from django.db import models

# Create your models here.

class GiroNegocioModel(models.Model):
    giroNegId = models.CharField(primary_key=True, null=False, db_column='C_GiroNeg', unique=True, max_length=6)

    giroNegNombre = models.CharField(max_length=200, null=False, db_column='N_GirNeg')

    giroNegActiv = models.CharField(max_length=2, null=False, db_column='C_Activi')

    giroNegPadre = models.CharField(max_length=6, null=False, db_column='C_GirNeg_Padre')

    giroNegHoraIni = models.IntegerField(
        db_column='Q_GirNeg_HraIni', null=False, default=0)

    giroNegHoraFin = models.IntegerField(
        db_column='Q_GirNeg_HraFin', null=False, default=0)

    giroNegLogin = models.CharField(max_length=20, null=False, db_column='C_Usuari_Login')

    giroNegDigitFecha = models.DateTimeField(auto_now=True, db_column='D_GirNeg_FecDig')

    giroNegActivo = models.BooleanField(null=False, db_column='F_GirNeg_Activo')

    giroNegCIIU = models.CharField(max_length=20, null=False, db_column='C_GirNeg_CIIU')

    class Meta:
        db_table = 'S02GIRONEGOCIO'

class WebContribuyenteModel(models.Model):
    webContribId =  models.AutoField(
        primary_key=True, null=False, db_column='IdContribuyente', unique=True)
    
    webContribTipPersona = models.IntegerField(
        db_column='TipoPersona', null=False, default=0)    

    webContribTipDocumento = models.CharField(
        max_length=1, db_column='TipoDocumento', null=False)

    webContribNroDocumento = models.CharField(
        max_length=20, db_column='NumeroDocumento', null=False)

    webContribNomCompleto = models.CharField(
        max_length=250, db_column='NombreCompleto', null=False)

    webContribDireccion = models.CharField(
        max_length=500, db_column='Direccion', null=False)

    webContribCorreo = models.CharField(
        max_length=100, db_column='CorreoElectronico', null=False)

    webContribTelefono = models.CharField(
        max_length=15, db_column='TelefonoCelular', null=False)

    webContribCodigo = models.CharField(
        max_length=11, db_column='CodigoContribuyente', null=False)

    class Meta:
        db_table = 's17Web_Contribuyente'

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


    precalSolicitante = models.ForeignKey(
        to=WebContribuyenteModel, related_name='webContribPrecalif', db_column='idContribuyente', on_delete=models.PROTECT)

    # precalSolicitanteId = models.IntegerField(
    #     db_column='idContribuyente', null=False, default=0)

    precalDescripcion = models.TextField(db_column='descripcion', null=True)        

    def __str__(self):
        return str(self.precalId)

    class Meta:
        db_table = 'S17Web_LIC_PreCalificacion'


class PrecalGiroNegModel(models.Model):
    precalGiroNegId = models.AutoField(primary_key=True, null=False, db_column='idCiiuRiesgo', unique=True)

    precalGiroNegCIIU =  models.IntegerField(
        db_column='codigoCiiu', null=False, default=0)

    precalificacion = models.ForeignKey(
        to=PrecalificacionModel, related_name='precalificacionCIIU', db_column='fkPreCalificacion', on_delete=models.PROTECT)

    precalGiroNegEstado = models.CharField(
        max_length=1, db_column='estado', null=False)    

    giroNegocio =  models.ForeignKey(
        to=GiroNegocioModel, related_name='precalificacionGiroNeg', db_column='C_GiroNeg', on_delete=models.PROTECT)

    precalGiroNegDigitFecha = models.DateTimeField(auto_now=True, db_column='RecordCreateDate')

    precalGiroNegDigitUser = models.CharField(
        max_length=100, db_column='RecordCreateUser', null=False)

    precalGiroNegRecordEstado = models.CharField(
        max_length=1, db_column='RecordState', null=False)

    class Meta:
        db_table = 'S17Web_LIC_CiiuRiesgo'


class PrecalCuestionarioModel(models.Model):
    precalCuestId = models.AutoField(primary_key=True, null=False, db_column='idCuestionario', unique=True)

    precalificacion = models.ForeignKey(
        to=PrecalificacionModel, related_name='precalificacionCuest', db_column='fkPreCalificacion', on_delete=models.PROTECT)

    precalCuestPreguntaId =  models.IntegerField(
        db_column='fkpregunta', null=False, default=0)
    
    precalCuestPreguntaNombre = models.CharField(
        max_length=200, db_column='pregunta', null=False)    

    precalCuestRpta = models.CharField(
        max_length=100, db_column='respuesta', null=False)    

    precalCuestEstado = models.CharField(
        max_length=1, db_column='estado', null=False) 

    precalCuestDigitFecha = models.DateTimeField(auto_now=True, db_column='RecordCreateDate')

    precalCuestDigitUser = models.CharField(
        max_length=100, db_column='RecordCreateUser', null=False)

    precalCuestRecordEstado = models.CharField(
        max_length=1, db_column='RecordState', null=False)

    class Meta:
        db_table = 'S17Web_LIC_Cuestionario'


class PrecalTipoDocumModel(models.Model):
    precalTipDocId = models.AutoField(primary_key=True, null=False, db_column='C_TipoDocum', unique=True)

    precalTipDocNombre = models.CharField(
        max_length=200, db_column='N_TipoDocum', null=False)    

    class Meta:
        db_table = 'S17Web_LIC_TipoDocum'


class PrecalEvaluacionModel(models.Model):
    precalEvalId = models.AutoField(primary_key=True, null=False, db_column='C_Evaluacion', unique=True)

    precalificacion = models.ForeignKey(
        to=PrecalificacionModel, related_name='precalificacionEval', db_column='idPreCalificacion', on_delete=models.PROTECT)

    tipoEval = models.ForeignKey(
        to=TipoEvalModel, related_name='evaluacionTipo', db_column='C_TipEval', on_delete=models.PROTECT)

    precalEvalComent =  models.TextField(db_column='T_Eval_Coment', null=False, default='')

    precalEvalDigitUser = models.CharField(
        max_length=20, db_column='C_Usuari_Login', null=False)
        
    precalEvalDigitFecha = models.DateTimeField(auto_now=True, db_column='D_Usuari_FecDig')

    precalEvalDigitPC = models.CharField(
        max_length=20, db_column='N_Usuari_PC', null=False)

    class Meta:
        db_table = 'S17Web_LIC_Evaluacion'

class PrecalDocumentacionModel(models.Model):
    precalDocumId = models.AutoField(primary_key=True, null=False, db_column='C_Documentac', unique=True)

    evaluacion = models.ForeignKey(
        to=PrecalEvaluacionModel, related_name='documentacionEval', db_column='C_Evaluacion', on_delete=models.PROTECT)

    tipoDocum = models.ForeignKey(
        to=PrecalTipoDocumModel, related_name='documentacionTipo', db_column='C_TipoDocum', on_delete=models.PROTECT)

    class Meta:
        db_table = 'S17Web_LIC_Documentacion'