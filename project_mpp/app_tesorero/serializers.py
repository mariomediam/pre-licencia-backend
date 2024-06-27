from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

class UploadFileSerializer(serializers.Serializer):
    archivo = serializers.FileField(max_length=200, use_url=True)
    location = serializers.CharField(max_length=200)
    file_name = serializers.CharField(max_length=200)
    allowed_extensions = []

    def __init__(self, *args, **kwargs):
        # Extrae las extensiones permitidas de los argumentos de palabras clave, si están presentes
        self.allowed_extensions = kwargs.pop('allowed_extensions', ['pdf'])
        super(UploadFileSerializer, self).__init__(*args, **kwargs)

    def validate_archivo(self, value):
        """
        Valida que solo se puedan cargar archivos con las extensiones permitidas
        """
        archivo: InMemoryUploadedFile = value
        extension = archivo.name.split('.')[-1].lower()

        # Verificar si la extensión está en la lista de extensiones permitidas
        if extension not in self.allowed_extensions:
            raise serializers.ValidationError(f"Solo se aceptan archivos con las siguientes extensiones: {', '.join(self.allowed_extensions)}.")

        return value

    def save(self):
        archivo: InMemoryUploadedFile = self.validated_data.get("archivo")
        fs = FileSystemStorage(self.validated_data.get("location"))
        file = fs.save(self.validated_data.get("file_name"), archivo)
        fileurl = fs.generate_filename(file)
        return fileurl