from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from user.permissions import IsAdminUser, IsModUser
from .models import Article, Keyword, Refrence, Institution, Author
from .serializers import ArticleSerializer, KeywordSerializer, RefrenceSerializer, InstitutionSerializer, AuthorSerializer

class AriticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAdminUser, IsModUser,)

    queryset = Article.objects

    def get_queryset(self):
        return self.queryset.all()
    
    def update(self, request, *args, **kwargs):
        if kwargs.get('partial'):
            return super().update(request=request, *args, **kwargs)
        return Response({"detail": "Method 'PUT' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class KeywordViewSet(ModelViewSet):
    serializer_class = KeywordSerializer
    permission_classes = (IsAdminUser, IsModUser,)

    queryset = Keyword.objects

    def get_queryset(self):
        return self.queryset.all()

class RefrenceViewSet(ModelViewSet):
    serializer_class = RefrenceSerializer
    permission_classes = (IsAdminUser, IsModUser,)

    queryset = Refrence.objects

    def get_queryset(self):
        return self.queryset.all()

class InstitutionViewSet(ModelViewSet):
    serializer_class = InstitutionSerializer
    permission_classes = (IsAdminUser, IsModUser,)

    queryset = Institution.objects

    def get_queryset(self):
        return self.queryset.all()

class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminUser, IsModUser,)

    queryset = Author.objects

    def get_queryset(self):
        return self.queryset.all()