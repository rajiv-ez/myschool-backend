from rest_framework.routers import DefaultRouter
from .views import CategorieArticleViewSet, ArticleViewSet, DemandeActifViewSet

router = DefaultRouter()
router.register('categories', CategorieArticleViewSet)
router.register('articles', ArticleViewSet)
router.register('demandes', DemandeActifViewSet)

urlpatterns = router.urls