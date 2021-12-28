from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .authManager import ManejoUsuarios


# Create your models here.
class UsuarioModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        primary_key=True, db_column='C_Usuari_Login', unique=True, null=False, max_length=20)

    password = models.BinaryField(null=True, db_column='N_Usuari_Clave')

    n_usuari_nombre = models.CharField(max_length=60, db_column='N_Usuari_Nombre', null=False)

    is_active = models.BooleanField(default=False, db_column='F_Usuari_Activo')   

    is_staff = models.BooleanField(default=False, db_column='F_Usuari_Admin')

    d_usuari_fecini = models.DateTimeField(db_column='D_Usuari_FecIni', null=False)

    d_usuari_fecfin = models.DateTimeField(db_column='D_Usuari_FecFin', null=False)

    c_usuari_resp = models.CharField(max_length=20, db_column='C_Usuari_Resp', null=False)

    d_usuari_fecdig = models.DateTimeField(db_column='D_Usuari_FecDig', null=False)

    c_usucodi = models.CharField(max_length=4, db_column='C_Usucodi', null=True)

    c_usucold = models.CharField(max_length=6, db_column='C_UsuCold', null=True)

    f_usuari_snp = models.BooleanField(default=False, db_column='F_Usuari_SNP', null=True)

    m_usuari_dni = models.CharField(max_length=8, db_column='M_Usuari_DNI', null=True)

    n_usuari_resppc = models.CharField(max_length=20, db_column='N_Usuari_RespPC', null=True)

    n_usuari_clavesgad = models.CharField(max_length=150, db_column='N_Usuari_claveSGAD', null=True)

    f_usuari_fiscal = models.BooleanField(default=False, db_column='F_Usuari_Fiscal')

    last_login = models.DateTimeField(db_column='last_login', null=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = ManejoUsuarios()

    def __str__(self):
        return self.n_usuari_nombre

    def get_full_name(self):
        return self.n_usuari_nombre
 
    def get_short_name(self):
        return self.n_usuari_nombre

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True    
    
    class Meta:
        db_table = 'usuarios'
