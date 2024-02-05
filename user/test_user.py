from django.test import TestCase
from article.tests.factories import ArticleFactory
from rest_framework.test import APIClient
from rest_framework import status

from user.models import User

class PasswordChangeAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_password_change_success(self):
        request_data = {
            'old_password': 'testpassword',
            'new_password': 'newtestpassword',
            'confirm_new_password': 'newtestpassword'
        }

        response = self.client.post('/api/reset/', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserRegistrationAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_success(self):
        request_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        response = self.client.post('/api/register/', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserViewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.articles = ArticleFactory.create_batch(5)

    def test_add_favorite_article(self):
        request_data = {'favorite': 1}

        response = self.client.post('/api/user/', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_favorite_article(self):
        request_data = {'favorite': 1}

        self.user.favorites.add(1)

        response = self.client.patch('/api/user/', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_details(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

