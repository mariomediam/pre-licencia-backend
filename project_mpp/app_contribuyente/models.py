from django.db import models

# Create your models here.

'''
C001Cod_Cont	char	no	11
C001Cod_Ant_Cont	char	no	7
C001Nombre	varchar	no	150
C001Tip_Cont	char	no	2
C001Cod_Lug	char	no	9
C001Cod_Calle	char	no	4
C001Numero	char	no	4
C001Piso	char	no	2
C001Manzana	char	no	4
C001Lote	char	no	6
C001Dpto	char	no	4
C001Direc_Adic	varchar	no	70
F001Fec_Reg	datetime	no	8
C001Responsable	varchar	no	100
C001Motivo	varchar	no	800
C001Homonimia	char	no	1
C001Profesión	char	no	5
C001Sexo	char	no	1
D001FecNac	datetime	no	8
C001CondInmueble	char	no	3
F001Fec_Fallecimiento	date	no	3
'''


class ContribuyenteModel(models.Model):

    contId = models.CharField(primary_key=True, null=False, db_column='C001Cod_Cont', unique=True, max_length=11)

    contIdAnt = models.CharField(null=False, db_column='C001Cod_Ant_Cont', max_length=7)

    contNombre = models.CharField(null=False, db_column='C001Nombre', max_length=150)

    contTipo = models.CharField(null=False, db_column='C001Tip_Cont', max_length=2)

    contLugar = models.CharField(null=False, db_column='C001Cod_Lug', max_length=9)

    contCalle = models.CharField(null=False, db_column='C001Cod_Calle', max_length=4)

    contNumero = models.CharField(null=False, db_column='C001Numero', max_length=4)

    contPiso = models.CharField(null=False, db_column='C001Piso', max_length=2)

    contManzana = models.CharField(null=False, db_column='C001Manzana', max_length=4)

    contLote = models.CharField(null=False, db_column='C001Lote', max_length=6)

    contDpto = models.CharField(null=False, db_column='C001Dpto', max_length=4)

    contDirecAdic = models.CharField(null=False, db_column='C001Direc_Adic', max_length=70)

    contFecReg = models.DateTimeField(null=False, db_column='F001Fec_Reg', auto_now=True)

    contResponsable = models.CharField(null=False, db_column='C001Responsable', max_length=100)

    contMotivo = models.CharField(null=False, db_column='C001Motivo', max_length=800)   

    contHomonimia = models.CharField(null=False, db_column='C001Homonimia', max_length=1)

    contProfesion = models.CharField(null=False, db_column='C001Profesión', max_length=5)

    contSexo = models.CharField(null=False, db_column='C001Sexo', max_length=1)

    contFecNac = models.DateTimeField(null=False, db_column='D001FecNac', auto_now=True)

    contCondInmueble = models.CharField(null=False, db_column='C001CondInmueble', max_length=3)

    contFecFallecimiento = models.DateField(null=False, db_column='F001Fec_Fallecimiento', auto_now=True)

    class Meta:
        db_table = 'T001Contribuyente'        
        managed = False                
        ordering = ['contNombre']








