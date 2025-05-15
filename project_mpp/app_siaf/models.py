from django.db import models

class Sincronizacion(models.Model):
    idSincro = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    ultima_actualizacion = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Fecha de última actualización de los datos'
    )
    comentarios = models.TextField(null=True, blank=True)
    exitoso = models.BooleanField(
        default=False,
        db_column='exitoso',
        help_text='Indica si la sincronización fue exitosa'
    )

    class Meta:
        db_table = 'SINCRONIZACION'
        verbose_name = 'Sincronización'
        verbose_name_plural = 'Sincronizaciones'
        app_label = 'app_siaf'
        managed = True


class RegistroSincronizacion(models.Model):
    idSincroReg = models.AutoField(primary_key=True)
    sincronizacion = models.ForeignKey(
        Sincronizacion,
        on_delete=models.CASCADE,
        related_name='registros'
    )
    ano_eje = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='ANO_EJE'
    )
    mes_eje = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MES_EJE'
    )
    nivel_gobierno = models.TextField(
        null=True, blank=True,
        db_column='NIVEL_GOBIERNO'
    )
    nivel_gobierno_nombre = models.TextField(
        null=True, blank=True,
        db_column='NIVEL_GOBIERNO_NOMBRE'
    )
    sector = models.TextField(
        null=True, blank=True,
        db_column='SECTOR'
    )
    sector_nombre = models.TextField(
        null=True, blank=True,
        db_column='SECTOR_NOMBRE'
    )
    pliego = models.TextField(
        null=True, blank=True,
        db_column='PLIEGO'
    )
    pliego_nombre = models.TextField(
        null=True, blank=True,
        db_column='PLIEGO_NOMBRE'
    )
    sec_ejec = models.TextField(
        null=True, blank=True,
        db_column='SEC_EJEC'
    )
    ejecutora = models.TextField(
        null=True, blank=True,
        db_column='EJECUTORA'
    )
    ejecutora_nombre = models.TextField(
        null=True, blank=True,
        db_column='EJECUTORA_NOMBRE'
    )
    departamento_ejecutora = models.TextField(
        null=True, blank=True,
        db_column='DEPARTAMENTO_EJECUTORA'
    )
    departamento_ejecutora_nombre = models.TextField(
        null=True, blank=True,
        db_column='DEPARTAMENTO_EJECUTORA_NOMBRE'
    )
    provincia_ejecutora = models.TextField(
        null=True, blank=True,
        db_column='PROVINCIA_EJECUTORA'
    )
    provincia_ejecutora_nombre = models.TextField(
        null=True, blank=True,
        db_column='PROVINCIA_EJECUTORA_NOMBRE'
    )
    distrito_ejecutora = models.TextField(
        null=True, blank=True,
        db_column='DISTRITO_EJECUTORA'
    )
    distrito_ejecutora_nombre = models.TextField(
        null=True, blank=True,
        db_column='DISTRITO_EJECUTORA_NOMBRE'
    )
    sec_func = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='SEC_FUNC'
    )
    programa_ppto = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='PROGRAMA_PPTO'
    )
    programa_ppto_nombre = models.TextField(
        null=True, blank=True,
        db_column='PROGRAMA_PPTO_NOMBRE'
    )
    tipo_act_proy = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='TIPO_ACT_PROY'
    )
    tipo_act_proy_nombre = models.TextField(
        null=True, blank=True,
        db_column='TIPO_ACT_PROY_NOMBRE'
    )
    producto_proyecto = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='PRODUCTO_PROYECTO'
    )
    producto_proyecto_nombre = models.TextField(
        null=True, blank=True,
        db_column='PRODUCTO_PROYECTO_NOMBRE'
    )
    actividad_accion_obra = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='ACTIVIDAD_ACCION_OBRA'
    )
    actividad_accion_obra_nombre = models.TextField(
        null=True, blank=True,
        db_column='ACTIVIDAD_ACCION_OBRA_NOMBRE'
    )
    funcion = models.TextField(
        null=True, blank=True,
        db_column='FUNCION'
    )
    funcion_nombre = models.TextField(
        null=True, blank=True,
        db_column='FUNCION_NOMBRE'
    )
    division_funcional = models.TextField(
        null=True, blank=True,
        db_column='DIVISION_FUNCIONAL'
    )
    division_funcional_nombre = models.TextField(
        null=True, blank=True,
        db_column='DIVISION_FUNCIONAL_NOMBRE'
    )
    grupo_funcional = models.TextField(
        null=True, blank=True,
        db_column='GRUPO_FUNCIONAL'
    )
    grupo_funcional_nombre = models.TextField(
        null=True, blank=True,
        db_column='GRUPO_FUNCIONAL_NOMBRE'
    )
    meta = models.TextField(
        null=True, blank=True,
        db_column='META'
    )
    finalidad = models.TextField(
        null=True, blank=True,
        db_column='FINALIDAD'
    )
    meta_nombre = models.TextField(
        null=True, blank=True,
        db_column='META_NOMBRE'
    )
    departamento_meta = models.TextField(
        null=True, blank=True,
        db_column='DEPARTAMENTO_META'
    )
    departamento_meta_nombre = models.TextField(
        null=True, blank=True,
        db_column='DEPARTAMENTO_META_NOMBRE'
    )
    fuente_financiamiento = models.TextField(
        null=True, blank=True,
        db_column='FUENTE_FINANCIAMIENTO'
    )
    fuente_financiamiento_nombre = models.TextField(
        null=True, blank=True,
        db_column='FUENTE_FINANCIAMIENTO_NOMBRE'
    )
    rubro = models.TextField(
        null=True, blank=True,
        db_column='RUBRO'
    )
    rubro_nombre = models.TextField(
        null=True, blank=True,
        db_column='RUBRO_NOMBRE'
    )
    tipo_recurso = models.TextField(
        null=True, blank=True,
        db_column='TIPO_RECURSO'
    )
    tipo_recurso_nombre = models.TextField(
        null=True, blank=True,
        db_column='TIPO_RECURSO_NOMBRE'
    )
    categoria_gasto = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='CATEGORIA_GASTO'
    )
    categoria_gasto_nombre = models.TextField(
        null=True, blank=True,
        db_column='CATEGORIA_GASTO_NOMBRE'
    )
    tipo_transaccion = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='TIPO_TRANSACCION'
    )
    generica = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='GENERICA'
    )
    generica_nombre = models.TextField(
        null=True, blank=True,
        db_column='GENERICA_NOMBRE'
    )
    subgenerica = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='SUBGENERICA'
    )
    subgenerica_nombre = models.TextField(
        null=True, blank=True,
        db_column='SUBGENERICA_NOMBRE'
    )
    subgenerica_det = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='SUBGENERICA_DET'
    )
    subgenerica_det_nombre = models.TextField(
        null=True, blank=True,
        db_column='SUBGENERICA_DET_NOMBRE'
    )
    especifica = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='ESPECIFICA'
    )
    especifica_nombre = models.TextField(
        null=True, blank=True,
        db_column='ESPECIFICA_NOMBRE'
    )
    especifica_det = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='ESPECIFICA_DET'
    )
    especifica_det_nombre = models.TextField(
        null=True, blank=True,
        db_column='ESPECIFICA_DET_NOMBRE'
    )
    monto_pia = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MONTO_PIA'
    )
    monto_pim = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MONTO_PIM'
    )
    monto_certificado = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MONTO_CERTIFICADO'
    )
    monto_comprometido_anual = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MONTO_COMPROMETIDO_ANUAL'
    )
    monto_comprometido = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MONTO_COMPROMETIDO'
    )
    monto_devengado = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MONTO_DEVENGADO'
    )
    monto_girado = models.DecimalField(
        max_digits=20, decimal_places=2,
        null=True, blank=True,
        db_column='MONTO_GIRADO'
    )

    class Meta:
        db_table = 'SINCRONIZACION_DETALLE'
        verbose_name = 'Registro de Sincronización'
        verbose_name_plural = 'Registros de Sincronización'
        app_label = 'app_siaf'
        managed = True


#---------------------------------------

class EstadoProyectoInversion(models.Model):
    c_estado = models.AutoField(
        primary_key=True,
        db_column='c_estado'
    )
    n_estado_descrip = models.CharField(
        max_length=50,
        db_column='n_estado_descrip'
    )
    n_estado_color = models.CharField(
        max_length=7,
        db_column='n_estado_color'
    )

    class Meta:
        db_table = 'ESTADOS_PROYECTO_INVERSION'
        verbose_name = 'Estado de Proyecto de Inversión'
        verbose_name_plural = 'Estados de Proyectos de Inversión'


class ProyectoInversion(models.Model):
    c_proinv = models.AutoField(
        primary_key=True,
        db_column='c_proinv'
    )
    ano_eje = models.IntegerField(
        db_column='ANO_EJE'
    )
    c_proinv_codigo = models.CharField(
        max_length=10,
        db_column='c_proinv_codigo'
    )
    n_proinv_nombre = models.TextField(
        db_column='n_proinv_nombre'
    )
    c_usuari_login = models.CharField(
        max_length=20,
        db_column='c_usuari_login'
    )
    n_proinv_pc = models.CharField(
        max_length=20,
        db_column='n_proinv_pc'
    )
    d_proinv_fecdig = models.DateTimeField(
        db_column='d_proinv_fecdig'
    )

    class Meta:
        db_table = 'PROYECTOS_INVERSION'
        verbose_name = 'Proyecto de Inversión'
        verbose_name_plural = 'Proyectos de Inversión'


class ProgramacionProyectoInversion(models.Model):
    c_prgpro = models.AutoField(
        primary_key=True,
        db_column='c_prgpro'
    )
    proyecto = models.ForeignKey(
        ProyectoInversion,
        on_delete=models.CASCADE,
        db_column='c_proinv',
        related_name='programaciones'
    )
    m_prgpro_mes = models.IntegerField(
        db_column='m_prgpro_mes'
    )
    q_prgpro_financ = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='q_prgpro_financ'
    )
    p_prgpro_fisica = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='p_prgpro_fisica'
    )
    q_prgpro_caida = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='q_prgpro_caida'
    )
    q_prgpro_increm = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='q_prgpro_increm'
    )
    q_prgpro_riesgo = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='q_prgpro_riesgo'
    )
    t_prgpro_estsit = models.TextField(
        db_column='t_prgpro_estsit'
    )
    t_prgpro_coment = models.TextField(
        db_column='t_prgpro_coment'
    )
    estado = models.ForeignKey(
        EstadoProyectoInversion,
        on_delete=models.PROTECT,
        db_column='c_estado',
        related_name='programaciones'
    )
    c_usuari_login = models.CharField(
        max_length=20,
        db_column='c_usuari_login'
    )
    n_prgpro_pc = models.CharField(
        max_length=20,
        db_column='n_prgpro_pc'
    )
    d_prgpro_fecdig = models.DateTimeField(
        db_column='d_prgpro_fecdig'
    )

    class Meta:
        db_table = 'PROGRAMACION_PROYECTOS_INVERSION'
        verbose_name = 'Programación de Proyecto de Inversión'
        verbose_name_plural = 'Programaciones de Proyectos de Inversión'
