from django.test import TestCase

from ..models.author import Author
from ..documents.article import ArticleDocument
from .factories import ArticleFactory
#from ..serializers import ArticleSerializer

class ArticleTestCase(TestCase):
    def test_search(self):
        articles = ArticleFactory.create_batch(5)

        res = ArticleDocument.search().query("match", title=articles[4].title)
        assert(res.count())

        res2 = ArticleDocument.search().query("match", title='')
        self.assertEqual(res2.count(), 0)

        res3 = ArticleDocument.search().query('nested', path='authors', query={'match': {'authors.name': Author.objects.first().name}})
        assert(res3.count() > 0)