from rest_framework import serializers
from .models import Poste, ClauseContrat, Contrat, Absence, Paie, Pointage, PauseJournaliere

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = '__all__'

class ClauseContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClauseContrat
        fields = '__all__'

class ContratSerializer(serializers.ModelSerializer):
    clauses = ClauseContratSerializer(many=True, read_only=True)

    class Meta:
        model = Contrat
        fields = '__all__'

class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = '__all__'

class PaieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paie
        fields = '__all__'


class PauseJournaliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = PauseJournaliere
        fields = '__all__'

class PointageSerializer(serializers.ModelSerializer):
    pauses = PauseJournaliereSerializer(many=True, read_only=True)
    class Meta:
        model = Pointage
        fields = '__all__'