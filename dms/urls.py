from rest_framework.routers import DefaultRouter
from .views import (
    TypeArchiveViewSet, ArchiveViewSet, list_all_models, list_model_instances,
    ModeleDocumentViewSet, ChampsModeleViewSet, DocumentGenereViewSet,
)
from django.urls import path

router = DefaultRouter()
router.register('types-archives', TypeArchiveViewSet)
router.register('archives', ArchiveViewSet)
router.register('modeles-documents', ModeleDocumentViewSet)
router.register('champs-modeles', ChampsModeleViewSet)
router.register('documents-generes', DocumentGenereViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('models/', list_all_models, name='all-models'),
    path('list-model/<str:app_label>/<str:model_name>/', list_model_instances),
]