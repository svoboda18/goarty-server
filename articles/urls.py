from django.urls import re_path, include
from .views import AriticleViewSet, RelationAddDeleteView, KeywordViewSet, RefrenceViewSet, InstitutionViewSet, AuthorViewSet
from rest_framework import routers

articles = routers.DefaultRouter()
articles.register(r'', AriticleViewSet)

keywords = routers.DefaultRouter()
keywords.register(r'', KeywordViewSet)

refrences = routers.DefaultRouter()
refrences.register(r'', RefrenceViewSet)

institutions = routers.DefaultRouter()
institutions.register(r'', InstitutionViewSet)

authors = routers.DefaultRouter()
authors.register(r'', AuthorViewSet)

urlpatterns = [
    re_path(r'^articles/?', include(articles.urls)),
    re_path(r'^articles/(?P<pk>[^/]+)/(?P<relation>[^/]+)/?$', RelationAddDeleteView.as_view()),
    re_path(r'^keywords/?', include(keywords.urls)),
    re_path(r'^refrences/?', include(refrences.urls)),
    re_path(r'^institutions/?', include(institutions.urls)),
    re_path(r'^authors/?', include(authors.urls)),
]
