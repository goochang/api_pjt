from django.shortcuts import get_object_or_404, render
from .models import Account
from rest_framework.response import Response
from .serializers import (
    AccountSerializer,
    LoginSerializer,
    PasswordSerializer,
    AccountUpdateSerializer,
    AccountDeleteSerializer,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token  # Using Token Authentication
from django.contrib.auth.hashers import make_password  # 비밀번호 해싱
from rest_framework.decorators import permission_classes
from django.contrib.auth import logout as auth_logout
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import login as auth_login
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password


@api_view(["POST"])
def signin(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # 입력 데이터에서 사용자 인증
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            account = get_object_or_404(Account, username=username)
            if account is not None and account.is_active is False:
                return Response(
                    {"message": "This user is deactivated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            raise AuthenticationFailed("Invalid username or password.")

        # auth_login(request, user)

        # 인증 성공: Token 발급 (or JWT 발급)
        refresh = RefreshToken.for_user(user)

        # 응답 반환
        return Response(
            {
                "message": "Login successful.",
                "refreshToken": str(refresh),
                "accessToken": str(refresh.access_token),
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "name": user.name,  # Account 모델에 따라 수정
                    "nickname": user.nickname,
                },
                # "token": token.key,
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    print(request.data["refreshToken"])
    # auth_logout(request)
    try:
        # 현재 사용자의 refresh token을 블랙리스트에 추가
        refresh_token = RefreshToken(request.data["refreshToken"])
        refresh_token.blacklist()  # 토큰을 블랙리스트에 추가하여 만료 처리

        return Response({"detail": "Successfully logged out."}, status=200)
    except TokenError:
        return Response({"detail": "Invalid refresh token."}, status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def password_update(request):
    user = request.user
    if user.id is not None:
        serializer = PasswordSerializer(
            data=request.data, context={"user": request.user}
        )

        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data["password"]
            if check_password(password, user.password):
                return Response(
                    {"message": "It is the same as your current password."},
                    status=status.HTTP_201_CREATED,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_201_CREATED)

    return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)


class AccountAPIView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data["password"] = make_password(
                serializer.validated_data["password"]
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user

        if user.id is not None and user.is_active:
            serializer = AccountDeleteSerializer(
                instance=user, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data["password"]
                if check_password(password, user.password):
                    user.delete()
                    data = {"message": "user deleted."}
                    return Response(data, status=status.HTTP_200_OK)
                return Response(
                    {"message": "Password does not match."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)


class UsernameAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, username):
        print(request.user)
        user = request.user
        if user.id:
            account = get_object_or_404(Account, username=username)

            serializer = AccountSerializer(account)
            return Response(serializer.data)  # 직렬화된 데이터를 JSON으로 응답

        return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def put(self, request, username):
        user = request.user
        if user.id is not None and user.username == username:
            check_serializer = AccountUpdateSerializer(
                data=request.data, context={"user": request.user}
            )

            if check_serializer.is_valid(raise_exception=True):
                serializer = AccountUpdateSerializer(
                    instance=user,
                    data=request.data,
                    partial=True,
                    context={"user": request.user},
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(check_serializer.errors, status=status.HTTP_201_CREATED)

        return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)
