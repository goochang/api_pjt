from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.AccountAPIView.as_view(), name="account_signup"),
    path("login/", views.signin, name="account_signin"),
    path("logout/", views.logout, name="account_logout"),
    path("password/", views.password_update, name="account_password"),
    path("<str:username>/", views.UsernameAPIView.as_view(), name="account_profile"),
]
