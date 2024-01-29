from rest_framework import serializers
from .models import (Clase, Materia, Usuario, Transcripcion, Resumen)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'


class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'


class TranscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcripcion
        fields = '__all__'


class ResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resumen
        fields = '__all__'
