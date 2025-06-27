from rest_framework import serializers
from .models import (
    PreferenceUser, Annonce, LuParAnnonce,
    ConfigurationClasse, DispositionClasse, Place, DemandeChangementPlace,
)

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'

class LuParAnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuParAnnonce
        fields = '__all__'

class PreferenceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceUser
        fields = '__all__'
        read_only_fields = ['user']

# ConfigurationClasse, DispositionClasse, Place serializers

class ConfigurationClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationClasse
        fields = '__all__'

class DispositionClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispositionClasse
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class DemandeChangementPlaceSerializer(serializers.ModelSerializer): 
    class Meta:
        model = DemandeChangementPlace
        fields = '__all__'

class DispositionClasseFullSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True)

    class Meta:
        model = DispositionClasse
        fields = '__all__'
    
    def validate(self, data):
        seen_positions = set()
        for p in data['places']:
            pos = (p['rangee'], p['ligne'], p['place'])
            if pos in seen_positions:
                raise serializers.ValidationError(f"Doublon détecté pour la place {pos}")
            seen_positions.add(pos)
        return data

    def create(self, validated_data):
        places_data = validated_data.pop('places')
        disposition = DispositionClasse.objects.create(**validated_data)
        for place in places_data:
            Place.objects.create(disposition=disposition, **place)
        return disposition

    def update(self, instance, validated_data):
        places_data = validated_data.pop('places')
        instance.nom = validated_data.get('nom', instance.nom)
        instance.description = validated_data.get('description', instance.description)
        instance.est_actif = validated_data.get('est_actif', instance.est_actif)
        instance.save()

        Place.objects.filter(disposition=instance).delete()
        for place in places_data:
            Place.objects.create(disposition=instance, **place)
        return instance
