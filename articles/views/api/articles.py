from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from articles.models.article import Article
from articles.serializers import ArticleSerializer

class AriticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser, FormParser,)

    queryset = Article.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)