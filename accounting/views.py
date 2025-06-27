from rest_framework import viewsets
from .models import Paiement, Depense, FraisScolaire, FraisIndividuel
from .serializers import PaiementSerializer, DepenseSerializer, FraisScolaireSerializer, FraisIndividuelSerializer
from django.db.models import Q

class FraisScolaireViewSet(viewsets.ModelViewSet):
    #queryset = FraisScolaire.objects.all()
    serializer_class = FraisScolaireSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'staff'):
            return  FraisScolaire.objects.all()
        elif hasattr(user, 'tuteur'):
            enfants = user.tuteur.eleves.all()
            classe_ids = enfants.values_list('inscriptions__classe_session__classe_id', flat=True).distinct()
            session_ids = enfants.values_list('inscriptions__classe_session__session_id', flat=True).distinct()
            return FraisScolaire.objects.filter(
                session_id__in=session_ids
            ).filter( 
                Q(classes__id__in=classe_ids) | Q(concerne_toutes_classes=True)
            ).distinct()
        return FraisScolaire.objects.none()

class FraisIndividuelViewSet(viewsets.ModelViewSet):
    #queryset = Paiement.objects.all()
    serializer_class = FraisIndividuelSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'staff'):
            return Paiement.objects.all()
        elif hasattr(user, 'tuteur'):
            enfants = user.tuteur.eleves.all()
            return Paiement.objects.filter(inscription__eleve__in=enfants).distinct()
        return Paiement.objects.none()

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
