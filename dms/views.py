from rest_framework import viewsets, filters
from .models import TypeArchive, Archive, ModeleDocument, ChampsModele, DocumentGenere
from .serializers import (
    TypeArchiveSerializer, ArchiveSerializer, ArchiveDetailSerializer,
    ModeleDocumentSerializer, ChampsModeleSerializer, DocumentGenereSerializer
)

class TypeArchiveViewSet(viewsets.ModelViewSet):
    queryset = TypeArchive.objects.all()
    serializer_class = TypeArchiveSerializer

# class ArchiveViewSet(viewsets.ModelViewSet):
#     queryset = Archive.objects.all()
#     serializer_class = ArchiveSerializer


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all()
    #serializer_class = ArchiveDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['type_archive__nom']

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['list', 'retrieve']:
            print("ArchiveDetailSerializer")
            return ArchiveDetailSerializer
        
        print("ArchiveSerializer")
        return ArchiveSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type_id = self.request.query_params.get('type_archive')
        if type_id:
            queryset = queryset.filter(type_archive_id=type_id)
        return queryset
    

class ModeleDocumentViewSet(viewsets.ModelViewSet):
    queryset = ModeleDocument.objects.all()
    serializer_class = ModeleDocumentSerializer

class ChampsModeleViewSet(viewsets.ModelViewSet):
    queryset = ChampsModele.objects.all()
    serializer_class = ChampsModeleSerializer

from docxtpl import DocxTemplate
from django.conf import settings
import os
from rest_framework.decorators import action
from rest_framework import serializers

# views.py
class DocumentGenereViewSet(viewsets.ModelViewSet):
    queryset = DocumentGenere.objects.all()
    serializer_class = DocumentGenereSerializer

    def perform_create(self, serializer):
        instance = serializer.save(cree_par=self.request.user)
        modele = instance.modele
        chemin = modele.template.path
        doc = DocxTemplate(chemin)
        context = instance.donnees

        expected_tags = set(modele.champs.values_list('tag_name', flat=True))
        if not expected_tags.issubset(set(context.keys())):
            raise serializers.ValidationError("Certains tags du modèle ne sont pas remplis.")

        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'dms/documents/generated'), exist_ok=True)
        output_path = os.path.join(settings.MEDIA_ROOT, 'dms/documents/generated', f'document_{instance.pk}.docx')
        doc.render(context)
        doc.save(output_path)

        instance.fichier_genere.name = f'dms/documents/generated/document_{instance.pk}.docx'
        instance.save()

# Vue pour exposer les modèles disponibles

from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response

EXCLUDED_APPS = {"admin", "auth", "contenttypes", "sessions", "authtoken", "institutions", "saas_admin"}
@api_view(['GET'])
def list_all_models(request):
    result = {}
    for model in apps.get_models():
        app_label = model._meta.app_label
        if app_label in EXCLUDED_APPS:
            continue
        model_name = model.__name__
        fields = [field.name for field in model._meta.fields]
        if app_label not in result:
            result[app_label] = []
        result[app_label].append({"name": model_name, "fields": fields})
    return Response(result)

@api_view(['GET'])
def list_model_instances(request, app_label, model_name):
    try:
        Model = apps.get_model(app_label, model_name)
        if Model is None:
            return Response({"error": "Modèle non trouvé"}, status=404)

        instances = Model.objects.all()
        data = []
        for obj in instances:
            serialized = {"id": obj.pk, "txt": str(obj)}
            for field in obj._meta.fields:
                if field.name not in ["id", "txt"]:
                    #serialized[field.name] = getattr(obj, field.name, "")
                    value = getattr(obj, field.name, "")
                    # Gère les clés étrangères
                    if hasattr(field, 'remote_field') and field.remote_field:
                        #value = str(value)  # ou value.pk
                        value = value.pk
                    serialized[field.name] = value
            data.append(serialized)
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
