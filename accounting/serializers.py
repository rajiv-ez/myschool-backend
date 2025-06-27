from rest_framework import serializers
from .models import FraisScolaire, FraisIndividuel, Paiement, Depense

class FraisScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraisScolaire
        fields = '__all__'

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'


class FraisIndividuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraisIndividuel
        fields = '__all__'

class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = '__all__'
