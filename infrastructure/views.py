
from rest_framework import viewsets
from .models import Succursale, Batiment, Salle
from .serializers import SuccursaleSerializer, BatimentSerializer, SalleSerializer

class SuccursaleViewSet(viewsets.ModelViewSet):
    queryset = Succursale.objects.all()
    serializer_class = SuccursaleSerializer

class BatimentViewSet(viewsets.ModelViewSet):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer

class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
