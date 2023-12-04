from django.test import TestCase

from ..models.author import Author
from ..documents.article import ArticleDocument
from .factories import ArticleFactory
#from ..serializers import ArticleSerializer

class ArticleTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        article = ArticleFactory()
        self.assertEqual(str(article), article.title)
#class AuthorTestCase(TestCase)