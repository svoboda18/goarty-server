from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
from user.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Article

from .factories import ArticleFactory
from settings import BASE_DIR

class ArticleTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.mod_user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True, is_admin=True)

        self.token = AccessToken.for_user(self.user)
        self.mod_token = AccessToken.for_user(self.mod_user)
        self.admin_token = AccessToken.for_user(self.admin_user)

        self.articles = ArticleFactory.create_batch(5)

    def test_article_view_set_get(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_article_view_set_delete(self):
        self.client.force_authenticate(user=self.admin_user, token=self.admin_token)
        response = self.client.delete('/api/articles/2/')
        self.assertEqual(response.status_code, 204)

    def test_article_view_set_post(self):
        pdf_content = open(BASE_DIR / "article/tests/test.pdf", 'rb').read()
        pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")
        self.client.force_authenticate(user=self.admin_user, token=self.admin_token)
        response = self.client.post('/api/articles/', {'pdf': pdf_file}, format='multipart')
        self.assertEqual(response.status_code, 201)
        article = Article.objects.last()
        self.uploaded = article
        self.assertIsNotNone(article.pdf)
        self.assertEqual(article.title, "How to Teach Software Modeling")

    def test_article_view_set_patch(self):
        self.client.force_authenticate(user=self.mod_user, token=self.mod_token)
        response = self.client.patch('/api/articles/5/', {'title': 'test new title'})
        self.assertEqual(response.status_code, 200)
        article = Article.objects.last()
        self.assertEqual(article.title, 'test new title')

    def test_relation_add_delete_view(self):
        article_id = 1
        keyword_id = 3

        self.client.force_authenticate(user=self.mod_user, token=self.mod_token)
        response = self.client.post(f'/api/articles/{article_id}/keywords/', {'id': keyword_id})
        self.assertEqual(response.status_code, 200)
        article = Article.objects.filter(id=article_id).first()
        self.assertEqual(article.keywords.filter(id=keyword_id).first().id, keyword_id)

        self.client.force_authenticate(user=self.mod_user, token=self.mod_token)
        response = self.client.delete(f'/api/articles/{article_id}/keywords/', {'id': keyword_id})
        self.assertEqual(response.status_code, 200)
        article = Article.objects.filter(id=article_id).first()
        self.assertEqual(article.keywords.filter(id=keyword_id).first(), None)

    def test_dowload(self):
        self.client.force_authenticate(user=self.mod_user, token=self.mod_token)
        
        response = self.client.get('/uploaded_articles/test.pdf')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response)

