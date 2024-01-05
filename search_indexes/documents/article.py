from django_elasticsearch_dsl import Document, fields

from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer

from articles.models.article import Article

html_strip = analyzer(
    'html_strip',
    tokenizer="whitespace",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class ArticleDocument(Document):
    id = fields.IntegerField(attr='id')
    authors = fields.TextField(
        attr='authors_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )
    institutions = fields.TextField(
        attr='institutions_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )
    keywords = fields.TextField(
        attr='keywords_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )
    refrences = fields.TextField(
        attr='refrences_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )
    title = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = 'article'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Article
        fields = [
            'body',
            'resume',
            'url',
            'created_at',
            'updated_at'
        ]