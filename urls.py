from django.contrib import admin
from django.urls import include, re_path

from articles import urls as articles_urls
from search_indexes import urls as search_index_urls
from user import urls as user_urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

apipatterns = [
    re_path(r'^user/?', include(user_urls)),
    re_path(r'', include(articles_urls)),
    re_path(r'^token/?', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/?', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^search/?', include(search_index_urls)),
]

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^api/?', include(apipatterns))
]
