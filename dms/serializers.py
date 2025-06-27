from django.forms import ValidationError
from rest_framework import serializers
from .models import TypeArchive, Archive, ModeleDocument, ChampsModele, DocumentGenere

class TypeArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeArchive
        fields = '__all__'

def get_instance_data(obj):
    if not obj.type_archive or not obj.type_archive.nom_modele:
        return None
    try:
        Model = apps.get_model(app_label=obj.type_archive.app_label, model_name=obj.type_archive.nom_modele)
        instance = Model.objects.filter(id=obj.objet_id).first()
        return str(instance) if instance else None
    except Exception:
        return None

class ArchiveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Archive
        fields = '__all__'
        read_only_fields = ('date_creation', 'date_modification', 'cree_par', 'modifie_par')

    def validate(self, data):
        errors = {}

        if not data.get('type_archive'):
            errors['type_archive'] = 'Ce champ est requis.'

        if not data.get('objet_id'):
            errors['objet_id'] = 'Ce champ est requis.'

        if not self.instance and not data.get('fichier'):
            errors['fichier'] = 'Un fichier est requis pour créer une archive.'

        if errors:
            raise serializers.ValidationError(errors)

        print("Validated data:", data)
        return data

    def create(self, validated_data):
        print("Creating archive with data:", validated_data)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['cree_par'] = request.user
            validated_data['modifie_par'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['modifie_par'] = request.user
        return super().update(instance, validated_data)
    
    
    def get_instance_data(self, obj):
        return get_instance_data(obj)

from django.apps import apps
class ArchiveDetailSerializer(serializers.ModelSerializer):
    instance_data = serializers.SerializerMethodField()

    class Meta:
        model = Archive
        fields = '__all__'

    def get_instance_data(self, obj):
        return get_instance_data(obj)


class ModeleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeleDocument
        fields = '__all__'

class ChampsModeleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampsModele
        fields = '__all__'


class DocumentGenereSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentGenere
        fields = '__all__'
        read_only_fields = ['cree_par', 'fichier_genere', 'date_generation']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['cree_par'] = request.user
        return super().create(validated_data)


