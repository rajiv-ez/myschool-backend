from rest_framework import serializers
from .models import CategorieArticle, Article, DemandeActif

class CategorieArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieArticle
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class DemandeActifSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeActif
        fields = '__all__'
