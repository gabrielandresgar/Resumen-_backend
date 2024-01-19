from rest_framework import serializers
from .models import (Clase, Materia, Usuario)

#  Los serializadores permiten convertir datos complejos como las instancias de modelo de Django y consultas
#  de conjuntos de datos en tipos de datos nativos de Python que luego pueden ser fácilmente renderizados en JSON o XML
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
