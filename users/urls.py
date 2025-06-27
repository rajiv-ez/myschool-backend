from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    TenantLoginView, MeView,
    UserViewSet, StaffViewSet, TuteurViewSet,
    EleveViewSet, RelationEleveTuteurViewSet,
    EleveDetailViewSet, TuteurDetailViewSet, StaffDetailViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'staffs', StaffViewSet)
router.register(r'staffs-details', StaffDetailViewSet, basename='staff-details')
router.register(r'tuteurs', TuteurViewSet)
router.register(r'tuteurs-details', TuteurDetailViewSet, basename='tuteur-details')
router.register(r'eleves', EleveViewSet)
router.register(r'eleves-details', EleveDetailViewSet, basename='eleve-details')
router.register(r'relations', RelationEleveTuteurViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('login/', TenantLoginView.as_view(), name='users-login'),
    path('me/', MeView.as_view(), name='users-me'),
]
