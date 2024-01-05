from django.test import TestCase

from ..serializers import ArticleSerializer
from .factories import ArticleFactory

class ArticleTestCase(TestCase):
    def _test_model_fields(self):
        """Serializer data matches the Article object for each field."""
        article = ArticleFactory()
        serializer = ArticleSerializer(article)
        for field_name in [
            'id', 'title', 'body', 'resume', 'url' #, 'authors', 'keywords', 'institutions', 'refrences' FIXME
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(article, field_name)
            )