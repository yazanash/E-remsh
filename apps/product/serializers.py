from rest_framework import serializers
from .models import Product, Category, Like, WishList, ProductItems, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    likes_count = serializers.IntegerField(source='like_set.count', read_only=True)
    liked = serializers.SerializerMethodField()
    wishlisted = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'offer', 'thumbnail',
                  'category', 'category_name', 'likes_count', 'liked', 'wishlisted']
        extra_kwargs = {
            'thumbnail': {'required': False}  # Make 'thumbnail' optional
        }

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


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItems
        fields = ['id', 'color', 'size']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_url', 'id']
