from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from es.models.article import Article

@registry.register_document
class ArticleDocument(Document):
    authors = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    institutions = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    keywords = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    refrences = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })

    class Index:
        name = 'article'

    class Django:
         model = Article
         fields = [
             'title',
             'body',
             'resume',
             'url',
             'created_at',
             'updated_at'
         ]