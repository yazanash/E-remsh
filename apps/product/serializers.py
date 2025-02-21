from rest_framework import serializers

from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    likes_count = serializers.IntegerField(source='like_set.count', read_only=True)
    class Meta:
        model = Product
        fields=['id' ,'name' ,'description','colors' ,'sizes' ,'price' ,'offer','thumbnail',
        'category' , 'likes_count', 'liked', 'wishlisted']


    def get_liked(self, obj):
        return getattr(obj, 'liked', False)

    def get_wishlisted(self, obj):
        return getattr(obj, 'wishlisted', False)