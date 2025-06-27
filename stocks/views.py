from rest_framework import viewsets
from .models import CategorieArticle, Article, DemandeActif
from .serializers import CategorieArticleSerializer, ArticleSerializer, DemandeActifSerializer

class CategorieArticleViewSet(viewsets.ModelViewSet):
    queryset = CategorieArticle.objects.all()
    serializer_class = CategorieArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class DemandeActifViewSet(viewsets.ModelViewSet):
    queryset = DemandeActif.objects.all()
    serializer_class = DemandeActifSerializer