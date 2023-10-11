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


class TipoLicenciaModel(models.Model):

    tipoLicId = models.CharField(primary_key=True, null=False, db_column='C_TIPLIC', unique=True, max_length=1)

    tipoLicDescrip = models.CharField(max_length=200, null=False, db_column='C_TIPLIC_DESCRIP')

    tipoLicSimula = models.BooleanField(null=False, db_column='F_TipLic_Simula')

    tipoLicNombre = models.CharField(max_length=200, null=False, db_column='n_tiplic_nombre')
    
    class Meta:
        db_table = 'S02TIPOLICENCIA'



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

    precalCorreo = models.CharField(
        max_length=150, db_column='correo', null=False)       

    precalTelefono = models.CharField(
        max_length=15, db_column='telefono', null=False)       

    tipoLicencia =  models.ForeignKey(
        to=TipoLicenciaModel, related_name='precalificacionTipoLicencia', db_column='C_TipLic', on_delete=models.PROTECT, null=True)     

    tipoTramiteId = models.CharField(
        max_length=8, db_column='C_TipTra', null=True)       

    tipoTramiteOrigen = models.CharField(
        max_length=1, db_column='F_TipTra_Origen', null=True)       

    tipoTramiteAnio = models.CharField(
        max_length=4, db_column='C_TipTra_Anio', null=True)   

    precalIdUsuarioContrib = models.IntegerField(db_column='idUsuarioContribuyente', null=False, default=0)    

    precalNombreComercial = models.CharField(
        max_length=16, db_column='nombreComercial', null=True)   

    precalDlVbEval = models.IntegerField(db_column='DL_vbEval', null=False, default=0)    

    precalSoliciSimulacion = models.CharField(
        max_length=5, db_column='C_Solici', null=True)   

    precalDlVbObs = models.CharField(
        max_length=1000, db_column='DL_vbObs', null=True)   

    precalDcVbEval = models.IntegerField(db_column='DC_vbEval', null=False, default=0)    

    precalDcVbObs = models.CharField(
        max_length=1000, db_column='DC_vbObs', null=True)   

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

    precalEvalComent =  models.TextField(db_column='T_Eval_Coment', null=True, blank=True, default='')

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



class SectoresLicModel(models.Model):
    sectorLicId = models.AutoField(primary_key=True, null=False, db_column='C_Sector', unique=True)

    sectorLicNombre = models.CharField(
        max_length=50, db_column='N_Sector', null=False)    

    class Meta:
        db_table = 'S17Web_LIC_Sectores'


class PrecalRequisitoArchivoModel(models.Model):
    precalArchivoId = models.AutoField(primary_key=True, null=False, db_column='idRequisitoArchivo', unique=True)

    precalificacion = models.ForeignKey(
        to=PrecalificacionModel, related_name='precalificacionReqArch', db_column='fkPreCalificacion', on_delete=models.PROTECT)

    precalAnexo = models.CharField(
        max_length=300, db_column='anexo', null=False)    

    precalRequisito = models.CharField(
        max_length=2, db_column='idRequisito', null=False)    

    precalRuta = models.CharField(
        max_length=150, db_column='ruta', null=False)

    precalNroFolio = models.IntegerField(
        db_column='numeroFolio', null=False, default=0)

    precalEnlace = models.TextField(db_column='enlace', null=True)  

    precalObserv = models.CharField(
        max_length=300, db_column='observacion', null=False) 

    precalCreate = models.DateTimeField(auto_now=True, db_column='RecordCreateDate')

    precalUser = models.CharField(
        max_length=100, db_column='RecordCreateUser', null=False) 

    precalState = models.CharField(
        max_length=1, db_column='RecordState', null=False) 
    
    class Meta:
        db_table = 'S17Web_LIC_Requisito_Archivo'

class PrecalFirmaArchivoModel(models.Model):
    precalFirmaId = models.AutoField(primary_key=True, null=False, db_column='C_FileFirma', unique=True)

    requisitoArchivo = models.ForeignKey(
        to=PrecalRequisitoArchivoModel, related_name='requisitoArchivoFirma', db_column='idRequisitoArchivo', on_delete=models.PROTECT)

    precalFirmaOrd = models.IntegerField(
        db_column='C_FileFirma_Ord', null=False, default=0)

    precalFirmaNombre = models.CharField(
        max_length=100, db_column='N_FileFirma_Nombre', null=False) 

    precalFirmaRuta = models.CharField(
        max_length=150, db_column='N_FileFirma_Ruta', null=False) 

    precalFirmaLogin = models.CharField(
        max_length=20, db_column='C_Usuari_Login', null=False)

    precalFirmaDigitFecha = models.DateTimeField(auto_now=True, db_column='D_FileFirma_FecDig')

    precalFirmaEstado = models.CharField(
        max_length=1, db_column='F_FileFirma_Estado', null=False) 
    
    class Meta:
        db_table = 'S17Web_LIC_Firma_Archivo'

class PrecalVBExpedienteModel(models.Model):
    precalVBExp = models.AutoField(primary_key=True, null=False, db_column='C_VBExp', unique=True)

    precalificacion = models.ForeignKey(
        to=PrecalificacionModel, related_name='precalificacionVBExp', db_column='idPreCalificacion', on_delete=models.PROTECT)

    tipoEval = models.ForeignKey(
        to=TipoEvalModel, related_name='vbExpedTipoEval', db_column='C_TipEval', on_delete=models.PROTECT)

    precalVBExpEval = models.CharField(
        max_length=1, db_column='F_VBExp_Eval', null=False)

    precalVBExpObs = models.CharField(
        max_length=400, db_column='T_VBExp_Obs', null=False)

    precalVBExpLogin = models.CharField(
        max_length=20, db_column='C_Usuari_Login', null=False)

    precalVBExpDigitFecha = models.DateTimeField(auto_now=True, db_column='F_VBExp_FecDig')

    class Meta:
        db_table = 'S17Web_LIC_VBExpediente'


class LicencGenModel(models.Model):
    soliciSimulacion = models.CharField(primary_key=True, null=False, max_length=5, db_column='C_Solici')

    soliciTasaCalculada = models.DecimalField(
        db_column='Q_LicGen_TasCal', max_digits=18, decimal_places=4, null=False)
    
    class Meta:
        db_table = 'S02LicencGen'        


class LicencArchivoModel(models.Model):
    licencFile = models.AutoField(primary_key=True, null=False, db_column='C_Licenc_File', unique=True)

    licencNro = models.CharField(max_length=6, db_column='C_Licenc', null=False)

    licencOrigen = models.CharField(max_length=1, db_column='F_Licencia_Origen', null=False)

    licencOrdRenov = models.CharField(max_length=2, db_column='C_Licenc_OrdRenov', null=False)

    licencFileNombre = models.CharField(max_length=100, db_column='N_Licenc_Nombre', null=False)

    licencFileRuta = models.CharField(max_length=150, db_column='N_Licenc_Ruta', null=False)

    licencEstado = models.CharField(max_length=1, db_column='F_Licenc_Estado', null=False, default="1")

    licencEmail = models.CharField(max_length=100, db_column='N_Licenc_Email', null=False, default="")

    licencFileLogin = models.CharField(max_length=20, db_column='C_Usuari_Login', null=False)

    licencFileDigitFecha = models.DateTimeField(auto_now=True, db_column='D_Licenc_FecFig')


    class Meta:
        db_table = 'S02Licenc_Archivo'        


class LicencSolModel(models.Model):
    soliciSimulacion = models.CharField(primary_key=True, null=False, max_length=5, db_column='C_Solici')

    licencNro = models.CharField(max_length=6, db_column='C_Licenc', null=False)

    licencOrigen = models.CharField(max_length=1, db_column='F_Licencia_Origen', null=False)

    licencOrdRenov = models.CharField(max_length=2, db_column='C_Licenc_OrdRenov', null=False)
    
    class Meta:
        db_table = 'S02LicencSol'



class LicProvTipoModel(models.Model):

    licProvTipoId = models.AutoField(primary_key=True, null=False, db_column='C_LicProv_Tipo', unique=True)

    licProvNombre = models.CharField(max_length=50, db_column='N_LicProv_Nombre', null=False)

    licProvDescrip = models.CharField(max_length=1024, db_column='T_LicProv_Descrip', null=False)

    licProvImagen = models.CharField(max_length=100, db_column='N_LicProv_Imagen', null=False)

    licProvIcon = models.CharField(max_length=50, db_column='N_LicProv_Icon', null=False)
    
    class Meta:
        db_table = 'S02Lic_Provisional_Tipo'

class LicProvUbicaModel(models.Model):

    ubicaId = models.AutoField(primary_key=True, null=False, db_column='C_Ubica', unique=True)

    licProvTipo = models.ForeignKey(to=LicProvTipoModel, related_name='licProvTipo_Ubica', db_column='C_LicProv_Tipo', on_delete=models.PROTECT)

    ubicaOrden = models.IntegerField(db_column='M_Ubica_Orden', null=False)

    ubicaCodigo = models.CharField(max_length=20, db_column='C_Ubica_Codigo', null=False)

    ubicaDescrip = models.CharField(max_length=512, db_column='N_Ubica_Descrip', null=False)

    ubicaUTMNorte = models.DecimalField(db_column='Q_Ubica_UTMNorte', max_digits=18, decimal_places=7, null=False)

    ubicaUTMEste = models.DecimalField(db_column='Q_Ubica_UTMEste', max_digits=18, decimal_places=7, null=False)

    ubicaLogin = models.CharField(max_length=20, null=False, db_column='C_Usuari_Login')

    ubicaDigitFecha = models.DateTimeField(auto_now=True, db_column='D_Ubica_FecDig')

    ubicaDigitPC = models.CharField(max_length=20, db_column='N_Ubica_PC', null=False)

    class Meta:
        db_table = 'S02Lic_Provisional_Ubica'

class LicProvRubroModel(models.Model):

    rubroId = models.AutoField(primary_key=True, null=False, db_column='C_Rubro', unique=True)

    licProvTipo = models.ForeignKey(to=LicProvTipoModel, related_name='licProvTipo_Rubro', db_column='C_LicProv_Tipo', on_delete=models.PROTECT)

    rubroOrden = models.IntegerField(db_column='M_Rubro_Orden', null=False)

    rubroDescrip = models.CharField(max_length=512, db_column='N_Rubro_Descrip', null=False)

    rubroDimension = models.CharField(max_length=50, db_column='N_Rubro_Dimension', null=False)

    rubroLogin = models.CharField(max_length=20, null=False, db_column='C_Usuari_Login')

    rubroDigitFecha = models.DateTimeField(auto_now=True, db_column='D_Rubro_FecDig')

    rubroDigitPC = models.CharField(max_length=20, db_column='N_Rubro_PC', null=False)

    class Meta:
        db_table = 'S02Lic_Provisional_Rubro'


class LicProvModel(models.Model):

    licProvId = models.AutoField(primary_key=True, null=False, db_column='C_LicProv', unique=True)

    licProvTipo = models.ForeignKey(to=LicProvTipoModel, related_name='licProvTipo_LicProv', db_column='C_LicProv_Tipo', on_delete=models.PROTECT)

    licProvNro  = models.IntegerField(db_column='M_LicProv_Nro', null=False)

    licProvRenov = models.IntegerField(db_column='M_LicProv_Renov', null=True)

    licProvExpNro = models.CharField(max_length=8, db_column='C_Exped', null=False)

    licProvExpAnio = models.CharField(max_length=4, db_column='C_Exped_Anio', null=False)

    licProvTitCod = models.CharField(max_length=11, db_column='C_LicProv_TitCod', null=False)

    licProvTitTipCod = models.CharField(max_length=2, db_column='C_LicProv_TitTipDoc', null=False)

    licProvTitNroDoc = models.CharField(max_length=11, db_column='M_LicProv_TitNroDoc', null=False)

    licProvTitImg = models.CharField(max_length=100, db_column='N_LicProv_TitImg', null=False)

    licProvRubro = models.ForeignKey(to=LicProvRubroModel, related_name='licProvRubro_licProv', db_column='C_Rubro', on_delete=models.PROTECT)

    licProvUbica = models.ForeignKey(to=LicProvUbicaModel, related_name='licProvUbica_licProv', db_column='C_Ubica', on_delete=models.PROTECT)

    licProvHorAte = models.CharField(max_length=50, db_column='N_LicProv_HorAte', null=False)

    licProvCerGas = models.CharField(max_length=50, db_column='N_LicProv_CerGas', null=False)

    licProvObs = models.CharField(max_length=1024, db_column='T_LicProv_Obs', null=False)

    licProvFecEmi = models.DateField(db_column='D_LicProv_FecEmi', null=False)

    licProvIniVig = models.DateField(db_column='D_LicProv_IniVig', null=False)

    licProvFinVig = models.DateField(db_column='D_LicProv_FinVig', null=False)

    licProvFormato = models.CharField(max_length=20, db_column='N_LicProv_Formato', null=False)

    licProvLogin = models.CharField(max_length=20, null=False, db_column='C_Usuari_Login')

    licProvDigitFecha = models.DateTimeField(auto_now=True, db_column='D_LicProv_FecDig')

    licProvDigitPC = models.CharField(max_length=20, db_column='N_LicProv_PC', null=False)

    class Meta:
        db_table = 'S02Lic_Provisional'


class LicProvAnulaModel(models.Model):

    licProv = models.OneToOneField(to=LicProvModel, primary_key=True, db_column='C_LicProv', on_delete=models.CASCADE, related_name='anulacion')

    anulaMotivo = models.CharField(max_length=1024, db_column='T_Anula_Motivo', null=False)

    anulaLogin = models.CharField(max_length=20, null=False, db_column='C_Usuari_Login')

    anulaDigitFecha = models.DateTimeField(auto_now=True, db_column='D_Anula_FecDig')

    anulaDigitPC = models.CharField(max_length=20, db_column='N_Anula_PC', null=False)

    class Meta:
        db_table = 'S02Lic_Provisional_Anula'




