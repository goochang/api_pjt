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
from rest_framework import filters
from django.db.models import Q


class ProductPagination(PageNumberPagination):
    page_query_param = "page"


class ProductListAPIView(APIView):
    pagination_class = ProductPagination
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author"]

    def get_queryset(self):
        """
        검색 및 필터링을 적용한 쿼리셋 반환
        """
        queryset = Product.objects.all()

        # 요청에서 검색 파라미터 가져오기
        search_query = self.request.query_params.get("search", None)

        # 검색 필터링 적용 (title, author)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(author__username__icontains=search_query)
                | Q(content__icontains=search_query)
            )

        return queryset

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

        queryset = self.get_queryset()

        # 페이징 적용
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 페이징 없이 전체 데이터 반환
        serializer = self.serializer_class(queryset, many=True)
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
