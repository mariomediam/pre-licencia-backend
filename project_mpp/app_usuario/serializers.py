from rest_framework import serializers

class MenuesSerializer(serializers.Serializer):
    menCodi = serializers.CharField(max_length=10, source='MenCodi')
    menDesc = serializers.CharField(max_length=100, source='MenDesc')
    menProg = serializers.CharField(max_length=100, source='MenProg')
    menKey = serializers.CharField(max_length=5, source='MenKey')
    menTipo = serializers.CharField(max_length=1, source='MenTipo')
    sysCodi = serializers.CharField(max_length=2, source='SysCodi')
    menMaestro = serializers.CharField(max_length=1, source='MenMaestro')
    acceso = serializers.IntegerField(source='Acceso')


class UserMenuesSerializer(serializers.Serializer):
    menCodi = serializers.CharField(max_length=10, source='MenCodi')
    usuCodi = serializers.CharField(max_length=20, source='UsuCodi')
    sysCodi = serializers.CharField(max_length=2, source='SysCodi')
    nuevo = serializers.BooleanField(source='Nuevo')
    modificar = serializers.BooleanField(source='Modificar')
    eliminar = serializers.BooleanField(source='Eliminar')
    imprimir = serializers.BooleanField(source='Imprimir')
    responsable = serializers.CharField(max_length=20, source='Responsable')
    pc = serializers.CharField(max_length=32, source='PC')
    fecDigit = serializers.DateTimeField(source='Fec_Digit')
