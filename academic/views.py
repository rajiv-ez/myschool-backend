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

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class PalierViewSet(viewsets.ModelViewSet):
    queryset = Palier.objects.all()
    serializer_class = PalierSerializer

class NiveauViewSet(viewsets.ModelViewSet):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer

class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer

class SpecialiteViewSet(viewsets.ModelViewSet):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer

class ClasseSessionViewSet(viewsets.ModelViewSet):
    queryset = ClasseSession.objects.all()
    serializer_class = ClasseSessionSerializer


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
