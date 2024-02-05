from article.tests.factories import ArticleFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from search_indexes.documents import ArticleDocument
from user.models import User
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk

class AriticleSearchViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.token = AccessToken.for_user(self.user)

        ArticleDocument.init()

        self.articles = ArticleFactory.create_batch(5)

        connections.get_connection().indices.refresh(index=ArticleDocument._index._name)

    def test_general_search(self):
        query = self.articles[0].title[:2].lower()

        self.client.force_authenticate(user=self.user, token=self.token)
        print('\n\nquery')
        print(query)
        response = self.client.get(f'/api/search/articles/?search={query}')
        print('\n\nquery')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.articles[0].title, count=1)

    def test_filter_keywords_in(self):
        keyword = 'language'

        self.client.force_authenticate(user=self.user, token=self.token)

        response = self.client.get(f'/api/search/articles/?keywords__in={keyword}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Python', count=1)
        self.assertContains(response, 'JavaScript', count=1)

    def test_filter_keywords_contains(self):
        keyword = 'script'
        self.client.force_authenticate(user=self.user, token=self.token)

        response = self.client.get(f'/api/search/articles/?keywords__contains={keyword}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'JavaScript', count=1)