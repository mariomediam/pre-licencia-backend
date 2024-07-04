from django.db import models

class TributoTipoOperacionModel(models.Model):
    C_TipOpe = models.CharField(primary_key=True, max_length=2)
    N_TipOpe = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        kwargs['using'] = 'BDSIGA'
        super(TributoTipoOperacionModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['using'] = 'BDSIGA'
        super(TributoTipoOperacionModel, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'TRIBUTO_TIPO_OPERACION'
        managed = False


class TributoArchivoModel(models.Model):
    C_Archivo = models.AutoField(primary_key=True)
    C_TipOpe = models.ForeignKey(TributoTipoOperacionModel, models.DO_NOTHING, db_column='C_TipOpe')
    M_Archivo_Anio = models.IntegerField(blank=True, null=True)
    M_Archivo_Mes = models.IntegerField(blank=True, null=True)
    D_Archivo_FecDig = models.DateTimeField()
    C_Usuari_Login = models.CharField(max_length=20)
    N_Archivo_PC = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        kwargs['using'] = 'BDSIGA'
        super(TributoArchivoModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['using'] = 'BDSIGA'
        super(TributoArchivoModel, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'TRIBUTO_ARCHIVO'
        managed = False

class TributoEmisionModel(models.Model):
    C_OpeFin = models.AutoField(primary_key=True)
    C_Archivo = models.ForeignKey(TributoArchivoModel, models.DO_NOTHING, db_column='C_Archivo')
    C_Emision_Contrib = models.CharField(max_length=11)
    N_Emision_Contrib = models.CharField(max_length=150)
    C_Emision_Partida = models.CharField(max_length=20)
    N_Emision_Partida = models.CharField(max_length=100)
    Q_Emision_Monto = models.DecimalField(max_digits=18, decimal_places=2)
    C_Emision_CtaCon = models.CharField(max_length=20)
    D_Emision_FecDig = models.DateTimeField()
    C_Usuari_Login = models.CharField(max_length=20)
    N_Emision_PC = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        kwargs['using'] = 'BDSIGA'
        super(TributoEmisionModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['using'] = 'BDSIGA'
        super(TributoEmisionModel, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'TRIBUTO_EMISION'
        managed = False