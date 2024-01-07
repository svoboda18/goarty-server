from rest_framework.serializers import SerializerMethodField
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ArticleDocument

class ArticleDocumentSerializer(DocumentSerializer):
    authors = SerializerMethodField()
    institutions = SerializerMethodField()
    keywords = SerializerMethodField()
    refrences = SerializerMethodField()

    class Meta:
        document = ArticleDocument
        fields = (
            'id', 'title', 'body', 'resume', 'url', 'authors', 'keywords', 'institutions', 'refrences', 'created_at',
            'updated_at'
        )

    def get_authors(self, obj):
        """Get authors."""
        if obj.authors:
            return list(obj.authors)
        else:
            return []
    
    def get_institutions(self, obj):
        """Get institutions."""
        if obj.institutions:
            return list(obj.institutions)
        else:
            return []
    
    def get_keywords(self, obj):
        """Get keywords."""
        if obj.keywords:
            return list(obj.keywords)
        else:
            return []
    
    def get_refrences(self, obj):
        """Get refrences."""
        if obj.refrences:
            return list(obj.refrences)
        else:
            return []