from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LivreViewSet, EmpruntViewSet

router = DefaultRouter()
router.register(r'livres', LivreViewSet)
router.register(r'emprunts', EmpruntViewSet)

urlpatterns = [
    path('', include(router.urls)),
]