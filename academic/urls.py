# academic/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    SessionViewSet, PalierViewSet, NiveauViewSet, FiliereViewSet, 
    SpecialiteViewSet, ClasseViewSet, ClasseSessionViewSet, InscriptionViewSet
)
router = DefaultRouter()
router.register(r'sessions', SessionViewSet)
router.register(r'paliers', PalierViewSet)
router.register(r'niveaux', NiveauViewSet)
router.register(r'filieres', FiliereViewSet)
router.register(r'specialites', SpecialiteViewSet)
router.register(r'classes', ClasseViewSet)
router.register(r'classe-sessions', ClasseSessionViewSet)
router.register(r'inscriptions', InscriptionViewSet)
urlpatterns = router.urls
