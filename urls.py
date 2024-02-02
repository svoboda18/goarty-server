from django.contrib import admin
from django.urls import include, re_path

from article import urls as articles_urls
from article.views import DownloadPDFView
from search_indexes import urls as search_index_urls
from user import urls as user_urls
from user.views import UsersViewSet

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

users = DefaultRouter()
users.register(r'', UsersViewSet)

apipatterns = [
    re_path(r'^user/?', include(user_urls)),
    re_path(r'^users/?', include(users.urls)),
    re_path(r'', include(articles_urls)),
    re_path(r'^token/?', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/?', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^search/?', include(search_index_urls)),
]

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^api/?', include(apipatterns)),
    re_path(r'^uploaded_articles/(?P<pdf>.*)$', DownloadPDFView.as_view())
]
