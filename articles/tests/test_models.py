from django.test import TestCase

from ..models.author import Author
from ..documents.article import ArticleDocument
from .factories import ArticleFactory
import requests

#from ..serializers import ArticleSerializer

class ArticleTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        article = ArticleFactory()
        self.assertEqual(str(article), article.title)
    def _test_article_upload(self):
        multipart_form_data = {
            'url': ('art.pdf', open('/workspaces/elasticsearch/art.pdf', 'rb')),
        }
        response = requests.post('http://127.0.0.1:8000/articles', files=multipart_form_data)

        print(response)

#class AuthorTestCase(TestCase)