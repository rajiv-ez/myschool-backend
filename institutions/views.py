
from rest_framework import viewsets
from institutions.serializers import ClientSerializer, DomainSerializer
from institutions.models import Client, Domain
from saas_admin.views import IsSaaSAdmin

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsSaaSAdmin]

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsSaaSAdmin]
