from rest_framework.serializers import ModelSerializer

from .models.article import Article

from .models.article import Author
from .models.article import Keyword
from .models.article import Institution
from .models.article import Refrence

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id', 'name'
        )

class KeywordSerializer(ModelSerializer):
    class Meta:
        model = Keyword
        fields = (
            'id', 'name'
        )

class InstitutionSerializer(ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'id', 'name'
        )

class RefrenceSerializer(ModelSerializer):
    class Meta:
        model = Refrence
        fields = (
            'id', 'name'
        )

class ArticleSerializer(ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    institutions = InstitutionSerializer(read_only=True, many=True)
    keywords = KeywordSerializer(read_only=True, many=True)
    refrences = RefrenceSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'body', 'resume', 'url', 'authors', 'keywords', 'institutions', 'refrences'
        )