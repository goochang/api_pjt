from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.signup, name="account_signup"),
    path("login/", views.signin, name="account_signin"),
    path("<str:username>/", views.profile, name="account_profile"),
    # path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
