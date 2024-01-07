from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from .views import UserModViewSet, UserRegistrationAPIView, UserViewAPI

mods = DefaultRouter()
mods.register(r'', UserModViewSet, basename='mods')

urlpatterns = [
	re_path(r'^register/?', UserRegistrationAPIView.as_view()),
    re_path(r'^mods/?', include(mods.urls)),
    re_path(r'^$', UserViewAPI.as_view()),
]