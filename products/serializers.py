from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()  # username 출력
    author_id = serializers.IntegerField(source="author.id", read_only=True)  # id 출력

    class Meta:
        model = Product
        fields = ["id", "title", "content", "photo", "author", "author_id"]

    def get_author(self, obj):
        # 작성자의 username 반환
        return obj.author.username if obj.author else None
