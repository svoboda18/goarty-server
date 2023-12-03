from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from es.models.article import Article

from es.models.author import Author
from es.models.keyword import Keyword
from es.models.institution import Institution
from es.models.refrence import Refrence

@registry.register_document
class ArticleDocument(Document):
    class Index:
        name = 'article'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    class Django:
         model = Article
         fields = [
             'title',
             'body',
             'resume',
             'url'
         ]
         related_models = [Author, Keyword, Refrence, Institution]
    def get_instances_from_related(self, related_instance):
        return related_instance.article