import os
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.serializers import ValidationError
from rest_framework import status

from django.http import HttpResponse

from user.permissions import IsModUser
from .models import Article, Keyword, Refrence, Institution, Author
from .serializers import ArticleSerializer, KeywordSerializer, RefrenceSerializer, InstitutionSerializer, AuthorSerializer
from settings import BASE_DIR

class AriticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser, FormParser,)

    queryset = Article.objects

    def get_queryset(self):
        return self.queryset.all()
    
    def update(self, request, *args, **kwargs):
        if kwargs.get('partial'):
            return super().update(request=request, *args, **kwargs)
        return Response({"detail": "Method 'PUT' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class RelationAddDeleteView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = (IsModUser,)

    def get_model(self, name):
        match name:
            case 'keyword': return Keyword
            case 'author': return Author
            case 'refrence': return Refrence
            case 'institution': return Institution
            case _: raise ValidationError({ 'detail': f'invalid relation {name}'})

    def validate_request(self, request, pk, relation):
        if not relation:
            raise ValidationError({ 'detail': 'no relation provided'})
        article = Article.objects.filter(id=pk).first()
        if not article:
            raise ValidationError({ 'detail': 'article not found'})
        model = self.get_model(relation[:-1])
        id = request.data.get('id')
        instance = model.objects.filter(id=id).first()
        if (instance is None):
            raise ValidationError({ 'detail': f'invalid {relation[:-1]} id {pk}'})
       
        return (article, instance)
    
    def post(self, request, pk, relation):
        article, instance = self.validate_request(request, pk, relation)
        
        field = getattr(article, relation)
        field.add(instance)

        ser = ArticleSerializer(instance=article)
        return Response(data=ser.data)
    def delete(self, request, pk, relation):
        article, instance = self.validate_request(request, pk, relation)
        
        field = getattr(article, relation)
        field.remove(instance)

        #TODO: should delete orphened objects
        #rels = instance.articles.all()
        #if len(rels) == 0:
        #    instance.delete()

        ser = ArticleSerializer(instance=article)
        return Response(data=ser.data)

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
