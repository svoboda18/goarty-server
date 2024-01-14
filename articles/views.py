import os
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from django.http import HttpResponse

from user.permissions import IsModUser
from .models import Article, Keyword, Refrence, Institution, Author
from .serializers import ArticleSerializer, KeywordSerializer, RefrenceSerializer, InstitutionSerializer, AuthorSerializer
from settings import BASE_DIR

class AriticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsModUser,)

    queryset = Article.objects

    def get_queryset(self):
        return self.queryset.all()
    
    def update(self, request, *args, **kwargs):
        if kwargs.get('partial'):
            return super().update(request=request, *args, **kwargs)
        return Response({"detail": "Method 'PUT' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class KeywordViewSet(ModelViewSet):
    serializer_class = KeywordSerializer
    permission_classes = (IsModUser,)

    queryset = Keyword.objects

    def get_queryset(self):
        return self.queryset.all()

class RefrenceViewSet(ModelViewSet):
    serializer_class = RefrenceSerializer
    permission_classes = (IsModUser,)

    queryset = Refrence.objects

    def get_queryset(self):
        return self.queryset.all()

class InstitutionViewSet(ModelViewSet):
    serializer_class = InstitutionSerializer
    permission_classes = (IsModUser,)

    queryset = Institution.objects

    def get_queryset(self):
        return self.queryset.all()

class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = (IsModUser,)

    queryset = Author.objects

    def get_queryset(self):
        return self.queryset.all()

class DownloadPDFView(APIView):
    def get(self, req, pdf):
        if pdf is None:
            return Response({"detail": "No file supplied"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        file_path = os.path.join(BASE_DIR, "uploaded_articles", pdf)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as fd:
                file_data = fd.read()

                response = HttpResponse(file_data, content_type='application/pdf')
                response['Content-Disposition'] = f"attachment; filename={os.path.basename(file_path)}"
                response['Content-Length'] = len(file_data)
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return response
        return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)
