
from rest_framework import serializers
from .models import Succursale, Batiment, Salle

class SuccursaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Succursale
        fields = '__all__'

class BatimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batiment
        fields = '__all__'

class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = '__all__'