from rest_framework import serializers

from .models import ProyectoInversion, ProgramacionProyectoInversion

class ProgramacionProyectoInversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramacionProyectoInversion
        fields = "__all__"

class ProyectoInversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoInversion
        fields = "__all__"
