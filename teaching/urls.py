from rest_framework.routers import DefaultRouter
from .views import (
    DomaineViewSet, UniteEnseignementViewSet, MatiereViewSet, MatiereGroupeeViewSet,
    EvenementViewSet, PresenceViewSet, NoteViewSet, NoteConfigViewSet
)

router = DefaultRouter()
router.register(r'domaines-enseignement', DomaineViewSet)
router.register(r'unites', UniteEnseignementViewSet)
router.register(r'matieres', MatiereViewSet)
router.register(r'matieres-groupees', MatiereGroupeeViewSet)
router.register(r'evenements', EvenementViewSet)
router.register(r'presences', PresenceViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'note-configs', NoteConfigViewSet)

urlpatterns = router.urls