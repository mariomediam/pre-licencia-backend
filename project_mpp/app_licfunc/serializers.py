from django.db.models import fields
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from django.conf import settings
from .models import PrecalificacionModel, TipoEvalModel, EvalUsuModel, WebContribuyenteModel, GiroNegocioModel, PrecalGiroNegModel, PrecalCuestionarioModel, PrecalTipoDocumModel, PrecalEvaluacionModel, PrecalDocumentacionModel, PrecalTipoDocumModel, TipoLicenciaModel, SectoresLicModel, PrecalRequisitoArchivoModel, PrecalFirmaArchivoModel, PrecalVBExpedienteModel
from app_licfunc.licfunc import ListarFunciones
import json


class GiroNegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiroNegocioModel
        fields = '__all__'

class TipoLicenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoLicenciaModel
        fields = '__all__'  

class WebContribuyenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebContribuyenteModel
        fields = '__all__'


class PrecalificacionSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PrecalificacionModel
        fields = '__all__'

class PrecalifContribSerializer(serializers.ModelSerializer):
    precalSolicitante = WebContribuyenteSerializer(read_only = True)
    precalFunciones = serializers.SerializerMethodField()

    def get_precalFunciones(self, obj):       
        return ListarFunciones(str(obj.precalFuncion))
    
    class Meta:
        model = PrecalificacionModel
        fields = '__all__'

class PrecalifGiroNegSerializer(serializers.ModelSerializer):
    precalificacion = PrecalificacionSerializer(read_only = True)
    giroNegocio = GiroNegocioSerializer(read_only = True)

    class Meta:
        model = PrecalGiroNegModel
        fields = '__all__'

class PrecalifCuestionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrecalCuestionarioModel
        fields = '__all__'


class TipoEvalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoEvalModel
        fields = '__all__'

class EvalUsuSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EvalUsuModel
        fields = '__all__'
        # depth = 1


class PrecalifUserEstadoSerializer(serializers.Serializer):
    precalId = serializers.IntegerField()
    precalDireccion = serializers.CharField(max_length=300)
    precalRiesgoEval = serializers.IntegerField()
    precalCompatCU = serializers.IntegerField()
    precalCompatDL = serializers.IntegerField()
    precalEstadoNom = serializers.SerializerMethodField(method_name='calcular_estado')
    webContribNomCompleto = serializers.CharField(max_length=250)

    def calcular_estado(self, instance):       
        estado_nombre = 'INDEFINIDO'

        if instance['precalRiesgoEval'] == 2 or instance['precalCompatCU'] == 2 or instance['precalCompatDL'] == 2:
            estado_nombre = 'RECHAZADO'
        elif instance['precalRiesgoEval'] == 1 and instance['precalCompatCU'] == 1 and instance['precalCompatDL'] == 1:
            estado_nombre = 'ACEPTADO'
        else:
            estado_nombre = "PENDIENTE"
        
        return estado_nombre


class PrecalTipoDocumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecalTipoDocumModel
        fields = '__all__'

class PrecalEvaluacionSerializer(serializers.ModelSerializer):      
    class Meta:
        model = PrecalEvaluacionModel
        fields = '__all__'
        

class PrecalEvaluacionTipoSerializer(serializers.ModelSerializer):
    precalificacion = PrecalificacionSerializer(read_only = True)
    precalEvalEstadoId = serializers.SerializerMethodField(method_name='calcular_estado')
    precalEvalEstadoNombre = serializers.SerializerMethodField(method_name='calcular_estado_nombre')    

    def calcular_estado(self, instance):       
        estado = 9

        if instance.tipoEval_id == 1:
            estado = instance.precalificacion.precalRiesgoEval
        elif instance.tipoEval_id == 2:
            estado = instance.precalificacion.precalCompatCU
        elif instance.tipoEval_id == 3:
            estado = instance.precalificacion.precalCompatDL
        
        return estado

    def calcular_estado_nombre(self, instance):       
        estado = 'Pendiente'

        if instance.tipoEval_id == 1:
            if instance.precalificacion.precalRiesgoEval == 1:
                estado = 'Aprobado'
            elif instance.precalificacion.precalRiesgoEval == 2:
                estado = 'Rechazado'
        elif instance.tipoEval_id == 2:
            if instance.precalificacion.precalCompatCU == 1:
                estado = 'Compatible'
            elif instance.precalificacion.precalCompatCU == 2:
                estado = 'No compatible'
        elif instance.tipoEval_id == 3:
            if instance.precalificacion.precalCompatDL == 1:
                estado = 'Aprobado'
            elif instance.precalificacion.precalCompatDL == 2:
                estado = 'Rechazado'
        
        return estado
    
    class Meta:
        model = PrecalEvaluacionModel
        fields = '__all__'

class PrecalDocumentacionSerializer(serializers.ModelSerializer):
    tipoDocum = PrecalTipoDocumSerializer(read_only = True)

    class Meta:
        model = PrecalDocumentacionModel
        fields = '__all__'


class DocumentacionSerializer(serializers.Serializer):
    precalTipDocId = serializers.IntegerField()

class ListDocumentacionSerializer(serializers.Serializer):
    documentos = DocumentacionSerializer(many=True)


class PrecalTipoDocumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecalTipoDocumModel
        fields = '__all__'


class UploadFileSerializer(serializers.Serializer):
    # max_length => indica el maximo de caracteres en el nombre de un archivo
    # use_url => si es True, el valor de la url sera usado para mostrar la ubicacion del archivo. si es False entonces se usara el nombre del archivo  (False es su valor x defecto)
    archivo = serializers.FileField(max_length=200, use_url=True)
    location = serializers.CharField(max_length=200)
    file_name = serializers.CharField(max_length=200)

    def validate(self, data):
        """
        Valida que el archivo no exista en la carpeta a crear
        """
        fs = FileSystemStorage(data['location'])
        if fs.exists(data['file_name']):
            raise serializers.ValidationError("El archivo {} ya existe".format(data['file_name']))

        return data

    def validate_archivo(self, value):
        """
        Valida que solo se puedan cargar archivos PDF
        """
        archivo: InMemoryUploadedFile = value
        
        if archivo.content_type != "application/pdf":
            raise serializers.ValidationError("Solo se pueden cargar archivos en formato PDF")

        """
        Valida tamaño máximo del archivo 10Mb
        """    
        if archivo.size > 10485760:
            raise serializers.ValidationError("El tamaño máximo del archivo es de 10Mb")

        return value

    def save(self):
        archivo: InMemoryUploadedFile = self.validated_data.get('archivo')
       
        # para ver el tipo de archivo que es
        # print(archivo.content_type)
        # # para ver el nombre del archivo
        # print(archivo.name)
        # # para ver el tamaño del archivo  expresado en bytes
        # print(archivo.size)
        # NOTA: una vez que se usa el metodo read() se elimina la informacion de ese archivo en la memoria RAM
        # ruta = default_storage.save(archivo.name, ContentFile(archivo.read()))
        # return settings.MEDIA_URL + ruta
        fs = FileSystemStorage(self.validated_data.get('location'))
        file = fs.save(self.validated_data.get('file_name'), archivo)            
        fileurl = fs.generate_filename(file)
        return fileurl

        

class SectoresLicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectoresLicModel
        fields = '__all__'     

class PrecalRequisitoArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecalRequisitoArchivoModel
        fields = '__all__'             

class PrecalFirmaArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecalFirmaArchivoModel
        fields = '__all__'             

class PrecalVBExpedienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecalVBExpedienteModel
        fields = '__all__'        
             