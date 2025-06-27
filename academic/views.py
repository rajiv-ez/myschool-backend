# academic/views.py
from rest_framework import viewsets
from .models import (
    Session, Palier, Niveau, Filiere, Specialite,
    Classe, ClasseSession, Inscription
)
from .serializers import (
    SessionSerializer, PalierSerializer, NiveauSerializer, 
    FiliereSerializer, SpecialiteSerializer,
    ClasseSerializer, ClasseSessionSerializer, InscriptionSerializer
)
from django_filters.rest_framework import DjangoFilterBackend

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class PalierViewSet(viewsets.ModelViewSet):
    queryset = Palier.objects.all()
    serializer_class = PalierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['session', ]

class NiveauViewSet(viewsets.ModelViewSet):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer

class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['niveau', ]

class SpecialiteViewSet(viewsets.ModelViewSet):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['filiere', ]

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['specialite', ]

class ClasseSessionViewSet(viewsets.ModelViewSet):
    queryset = ClasseSession.objects.all()
    serializer_class = ClasseSessionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['classe', 'session' ]


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['eleve', 'classe_session' ]
