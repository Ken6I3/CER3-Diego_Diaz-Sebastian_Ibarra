from rest_framework import serializers
from .models import Taller, Profesor, Lugar, Categoria

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ["id", "nombre_completo"]

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = ["id", "nombre"]

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]

class TallerSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer()
    lugar = LugarSerializer()
    categoria = CategoriaSerializer()

    class Meta:
        model = Taller
        fields = "__all__"