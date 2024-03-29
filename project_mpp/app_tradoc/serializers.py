from rest_framework import serializers
from .models import ExpedientesModel


# class PrecalifUserEstadoSerializer(serializers.Serializer):
#     precalId = serializers.IntegerField()
#     precalDireccion = serializers.CharField(max_length=300)
#     precalRiesgoEval = serializers.IntegerField()
#     precalCompatCU = serializers.IntegerField()
#     precalCompatDL = serializers.IntegerField()
#     precalDlVbEval = serializers.IntegerField()
#     precalDcVbEval = serializers.IntegerField()
#     webContribNomCompleto = serializers.CharField(max_length=250)
#     farchivos = serializers.IntegerField()

class ExpedientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpedientesModel
        fields = "__all__"        