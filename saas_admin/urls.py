from rest_framework.routers import DefaultRouter
from .views import InstitutionAdminViewSet, PublicLoginView
from institutions.views import ClientViewSet, DomainViewSet

router = DefaultRouter()
router.register(r'institution-admins', InstitutionAdminViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'domains', DomainViewSet)

# urlpatterns = router.urls

from django.urls import path, include
urlpatterns = [
    path('', include(router.urls)),
    path('admin/login/', PublicLoginView.as_view()),
]