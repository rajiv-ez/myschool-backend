from rest_framework.routers import DefaultRouter
from .views import (
    PosteViewSet, ClauseContratViewSet, ContratViewSet,
    AbsenceViewSet, PaieViewSet, PointageViewSet, PauseJournaliereViewSet
)

router = DefaultRouter()
router.register(r'postes', PosteViewSet)
router.register(r'clauses', ClauseContratViewSet)
router.register(r'contrats', ContratViewSet)
router.register(r'absences', AbsenceViewSet)
router.register(r'paies', PaieViewSet)
router.register(r'pointages', PointageViewSet)
router.register(r'pauses', PauseJournaliereViewSet)

urlpatterns = router.urls