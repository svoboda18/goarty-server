from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AriticleViewSet

articles = DefaultRouter()
articles.register(r'articles', AriticleViewSet, basename='search_articledocument')

urlpatterns = articles.urls
