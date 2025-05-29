from rest_framework import viewsets
from .models import Poste, ClauseContrat, Contrat, Absence, Paie, Pointage, PauseJournaliere
from .serializers import (
    PosteSerializer, ClauseContratSerializer, ContratSerializer,
    AbsenceSerializer, PaieSerializer, PointageSerializer, PauseJournaliereSerializer
)

class PosteViewSet(viewsets.ModelViewSet):
    queryset = Poste.objects.all()
    serializer_class = PosteSerializer

class ClauseContratViewSet(viewsets.ModelViewSet):
    queryset = ClauseContrat.objects.all()
    serializer_class = ClauseContratSerializer

class ContratViewSet(viewsets.ModelViewSet):
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer

class AbsenceViewSet(viewsets.ModelViewSet):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer

class PaieViewSet(viewsets.ModelViewSet):
    queryset = Paie.objects.all()
    serializer_class = PaieSerializer

class PointageViewSet(viewsets.ModelViewSet):
    queryset = Pointage.objects.all()
    serializer_class = PointageSerializer

class PauseJournaliereViewSet(viewsets.ModelViewSet):
    queryset = PauseJournaliere.objects.all()
    serializer_class = PauseJournaliereSerializer
