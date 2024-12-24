from django.shortcuts import get_object_or_404, render
from .models import Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_query_param = "page"


class ProductListAPIView(APIView):
    pagination_class = ProductPagination
    serializer_class = ProductSerializer

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    # 목록
    def get(self, request):
        Products = Product.objects.all()
        page = self.paginate_queryset(Products)
        print(page)
        if page is not None:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True).data
            )
        else:
            serializer = self.serializer_class(Products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # 등록
    @permission_classes([IsAuthenticated])
    def post(self, request):
        user = request.user
        print(user.id)
        request.data["author"] = user.id
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        Product = self.get_object(pk)
        serializer = ProductSerializer(Product)
        return Response(serializer.data)

    # 수정
    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        user = request.user
        Product = self.get_object(pk)
        if user.id == Product.author_id:
            serializer = ProductSerializer(Product, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Author only."}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        user = request.user
        Product = self.get_object(pk)
        if user.id == Product.author_id:
            Product.delete()
            data = {"pk": f"{pk} is deleted."}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Author only."}, status=status.HTTP_400_BAD_REQUEST
            )
