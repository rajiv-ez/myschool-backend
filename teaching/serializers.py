from rest_framework import serializers
from .models import (
    Domaine, UniteEnseignement, Matiere, MatiereGroupee, 
    Evenement, FichierEvenement, Presence, Exercice, FichierExercice, 
    Note, NoteConfig
)

class DomaineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domaine
        fields = '__all__'

class UniteEnseignementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniteEnseignement
        fields = '__all__'

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class MatiereGroupeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatiereGroupee
        fields = '__all__'

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

class FichierEvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichierEvenement
        fields = '__all__'

class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = '__all__'

class FichierExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichierExercice
        fields = '__all__'

class PresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class NoteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteConfig
        fields = '__all__'