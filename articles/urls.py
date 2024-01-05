from django.contrib import admin
from django.urls import include, path, re_path
from .views.api.articles import AriticleViewSet
from rest_framework import routers

from search_indexes import urls as search_index_urls

articles = routers.DefaultRouter()
articles.register(r'articles', AriticleViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('user.urls')),
    *articles.urls,
    re_path(r'^search/', include(search_index_urls)),
]
