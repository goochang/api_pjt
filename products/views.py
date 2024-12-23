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


class ProductListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        Products = Product.objects.all()
        serializer = ProductSerializer(Products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    # 두 번 이상 반복되는 로직은 함수로 빼면 좋습니다👀
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        Product = self.get_object(pk)
        serializer = ProductSerializer(Product)
        return Response(serializer.data)

    def put(self, request, pk):
        Product = self.get_object(pk)
        serializer = ProductSerializer(Product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        Product = self.get_object(pk)
        Product.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)


def Product_list_html(request):
    Products = Product.objects.all()
    context = {"Products": Products}
    return render(request, "Products/Products.html", context)


@api_view(["GET", "POST"])
def Product_list(request):
    if request.method == "GET":
        Products = Product.objects.all()
        serializer = ProductSerializer(Products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def Product_detail(request, pk):
    Product = get_object_or_404(Product, pk=pk)
    print(request.method)
    if request.method == "GET":
        serializer = ProductSerializer(Product)
        print("get")
        return Response(serializer.data)
    elif request.method == "PUT":
        print("put")
        serializer = ProductSerializer(Product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        print("delete")
        Product.delete()
        data = {"delete": f"Product({pk}) is deleted."}
        return Response(data, status=status.HTTP_200_OK)
