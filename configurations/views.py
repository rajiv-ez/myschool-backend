from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from .models import (
    PreferenceUser, Annonce, LuParAnnonce,
    ConfigurationClasse, DispositionClasse, Place, DemandeChangementPlace,
)
from .serializers import (
    PreferenceUserSerializer, AnnonceSerializer, LuParAnnonceSerializer,
    ConfigurationClasseSerializer, 
    DispositionClasseSerializer, DispositionClasseFullSerializer,
    PlaceSerializer, DemandeChangementPlaceSerializer
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categorie', 'etat', 'cible_global', 'classes']

class LuParAnnonceViewSet(viewsets.ModelViewSet):
    queryset = LuParAnnonce.objects.all()
    serializer_class = LuParAnnonceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'annonce']

class PreferenceUserViewSet(viewsets.ModelViewSet):
    serializer_class = PreferenceUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        pref, _ = PreferenceUser.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(pref)
        return Response(serializer.data)

    def get_queryset(self):
        #return PreferenceUser.objects.all()
        return PreferenceUser.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ConfigurationClasse, DispositionClasse, Place viewsets

class ConfigurationClasseViewSet(viewsets.ModelViewSet):
    queryset = ConfigurationClasse.objects.all()
    serializer_class = ConfigurationClasseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        classe_session_id = self.request.query_params.get('classe_session')
        if classe_session_id:
            queryset = queryset.filter(classe_session=classe_session_id)
        return queryset

    @action(detail=True, methods=["post"])
    def activer(self, request, pk=None):
        ConfigurationClasse.objects.update(est_active=False)
        instance = self.get_object()
        instance.est_active = True
        instance.save()
        return Response({"status": "Configuration activée", "id": instance.id})


@api_view(['GET'])
def configuration_complete(request, classe_session_id):
    try:
        config = ConfigurationClasse.objects.get(classe_session_id=classe_session_id, est_actif=True)
        disposition = config.dispositions.filter(est_actif=True).first()
        places = Place.objects.filter(disposition=disposition) if disposition else []

        return Response({
            'configuration': ConfigurationClasseSerializer(config).data,
            'disposition': DispositionClasseSerializer(disposition).data if disposition else None,
            'places': PlaceSerializer(places, many=True).data
        })
    except ConfigurationClasse.DoesNotExist:
        return Response({'detail': 'Aucune configuration active trouvée'}, status=404)
    
class DispositionClasseViewSet(viewsets.ModelViewSet):
    queryset = DispositionClasse.objects.all()
    serializer_class = DispositionClasseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        config_id = self.request.query_params.get('configuration')
        if config_id:
            queryset = queryset.filter(configuration=config_id)
        return queryset

    @action(detail=True, methods=["post"])
    def activer(self, request, pk=None):
        config_id = self.get_object().configuration_id
        DispositionClasse.objects.filter(configuration_id=config_id).update(est_active=False)
        instance = self.get_object()
        instance.est_active = True
        instance.save()
        return Response({"status": "Disposition activée", "id": instance.id})


class DispositionClasseFullViewSet(viewsets.ModelViewSet):
    queryset = DispositionClasse.objects.all()
    serializer_class = DispositionClasseFullSerializer

    @action(detail=True, methods=["post"])
    def activer(self, request, pk=None):
        config_id = self.get_object().configuration_id
        DispositionClasse.objects.filter(configuration_id=config_id).update(est_active=False)
        instance = self.get_object()
        instance.est_active = True
        instance.save()
        return Response({"status": "Disposition activée", "id": instance.id})

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class DemandeChangementPlaceViewSet(viewsets.ModelViewSet):
    queryset = DemandeChangementPlace.objects.all()
    serializer_class = DemandeChangementPlaceSerializer

    # def get_queryset(self):
    #     return DemandeChangementPlace.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
