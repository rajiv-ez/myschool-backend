from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaiementViewSet, DepenseViewSet, FraisScolaireViewSet, FraisIndividuelViewSet

router = DefaultRouter()
router.register(r'paiements', PaiementViewSet, basename='paiement')
router.register(r'frais-scolaires', FraisScolaireViewSet, basename='frais-scolaire')
router.register(r'frais-individuels', FraisIndividuelViewSet, basename='frais-individuels')
router.register(r'depenses', DepenseViewSet, basename='depense')

urlpatterns = [
    path('', include(router.urls)),
]