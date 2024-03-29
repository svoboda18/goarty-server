from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from .views import PasswordChangeAPIView, UserRegistrationAPIView, UserViewAPI

urlpatterns = [
	re_path(r'^register/?', UserRegistrationAPIView.as_view()),
    re_path(r'^reset/?', PasswordChangeAPIView.as_view()),
    re_path(r'^$', UserViewAPI.as_view()),
]