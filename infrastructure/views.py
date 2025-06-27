
from .models import Succursale, Batiment, Salle
from .serializers import SuccursaleSerializer, BatimentSerializer, SalleSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

class SuccursaleViewSet(viewsets.ModelViewSet):
    queryset = Succursale.objects.all()
    serializer_class = SuccursaleSerializer

class BatimentViewSet(viewsets.ModelViewSet):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['succursale']

class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['batiment']

