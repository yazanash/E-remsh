from rest_framework import serializers
from .models import Product, Category, Like, WishList


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    likes_count = serializers.IntegerField(source='like_set.count', read_only=True)
    liked = serializers.SerializerMethodField()
    wishlisted = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'colors', 'sizes', 'price', 'offer', 'thumbnail',
                  'category', 'likes_count', 'liked', 'wishlisted']

    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Like.objects.filter(user=user, product=obj).exists()
        return False

    def get_wishlisted(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return WishList.objects.filter(user=user, product=obj).exists()
        return False
