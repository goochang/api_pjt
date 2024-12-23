from django.shortcuts import get_object_or_404, render
from .models import Account
from rest_framework.response import Response
from .serializers import AccountSerializer, AccountDetailSerializer, LoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token  # Using Token Authentication
from django.contrib.auth.hashers import make_password  # 비밀번호 해싱
import json


# @csrf_exempt
@api_view(["POST"])
def signup(request):
    print("signup", request.data)
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.validated_data["password"] = make_password(
            serializer.validated_data["password"]
        )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def signin(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # 입력 데이터에서 사용자 인증
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid username or password.")

        # 인증 성공: Token 발급 (or JWT 발급)
        token, created = Token.objects.get_or_create(user=user)

        # 응답 반환
        return Response(
            {
                "message": "Login successful.",
                "token": token.key,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "name": user.name,  # Account 모델에 따라 수정
                    "nickname": user.nickname,
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def profile(request, username):
    account = get_object_or_404(Account, username=username)

    serializer = AccountSerializer(account)  # 객체를 직렬화
    return Response(serializer.data)  # 직렬화된 데이터를 JSON으로 응답
