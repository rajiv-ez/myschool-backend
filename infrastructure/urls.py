
from rest_framework.routers import DefaultRouter
from .views import SuccursaleViewSet, BatimentViewSet, SalleViewSet

router = DefaultRouter()
router.register(r'succursales', SuccursaleViewSet)
router.register(r'batiments', BatimentViewSet)
router.register(r'salles', SalleViewSet)

urlpatterns = router.urls