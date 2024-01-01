from django.urls import path
from .views import (
	UserRegistrationAPIView,
    UserLoginAPIView,
    UserLogoutViewAPI,
    UserViewAPI,

)


urlpatterns = [
	path('user/register/', UserRegistrationAPIView.as_view()),
    path('user/login/', UserLoginAPIView.as_view()),
    path('user/', UserViewAPI.as_view()),
    path('user/logout/', UserLogoutViewAPI.as_view()),
]