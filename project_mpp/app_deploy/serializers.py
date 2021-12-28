#from django.db.models import fields
from rest_framework import serializers

class SelectTrabajadorSerializer(serializers.Serializer):
    field = serializers.CharField(required=True, max_length=30, error_messages={'required': 'Debe ingresar opción de búsqueda'})
    valor_buscado = serializers.CharField(required=True, max_length=50, error_messages={'required': 'Debe ingresar valor buscado'})

class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField(required=True, max_length=20, error_messages={'required': 'Debe ingresar usuario de sistema'})
    password = serializers.CharField(required=True, max_length=50, error_messages={'required': 'Debe ingresar password'})    