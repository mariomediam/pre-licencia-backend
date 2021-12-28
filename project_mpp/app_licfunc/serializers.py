from django.db.models import fields
from rest_framework import serializers
from .models import PrecalificacionModel, TipoEvalModel, EvalUsuModel

class PrecalificacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PrecalificacionModel
        fields = '__all__'

class TipoEvalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoEvalModel
        fields = '__all__'

class EvalUsuSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EvalUsuModel
        fields = '__all__'
        depth = 1