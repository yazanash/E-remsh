from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.

@api_view(['GET'])
def get_products(request):
    filter_set= ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filter_set.qs.count()
    resPage=1
    pages_count=count/resPage
    paginator = PageNumberPagination()
    paginator.page_size=resPage

    query_set= paginator.paginate_queryset(filter_set.qs,request)

    for product in query_set:
        product.liked = Like.objects.filter(user=user, product=product).exists()
        product.wishlisted = Wishlist.objects.filter(user=user, product=product).exists()

    serializer = ProductSerializer(query_set,many=True,context={'request': request})
    return Response({"products":serializer.data,"pages":int(pages_count)})

@api_view(['GET'])
def get_product_by_id(request,id):
    product = get_object_or_404(Product,id=id)
    serializer = ProductSerializer(product,many=False)
    return Response({"products":serializer.data})

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response({"categories":serializer.data})


@api_view(['POST'])
def like_product(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if Like.objects.filter(user=user, product=product).exists():
        return Response({'detail': 'You have already liked this product.'}, status=status.HTTP_400_BAD_REQUEST)

    Like.objects.create(user=user, product=product)
    return Response({'detail': 'Product liked successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def unlike_product(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    try:
        like = Like.objects.get(user=user, product=product)
        like.delete()
        return Response({'detail': 'Product unliked successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response({'detail': 'You have not liked this product yet.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if Wishlist.objects.filter(user=user, product=product).exists():
        return Response({'detail': 'This product is already in your wishlist.'}, status=status.HTTP_400_BAD_REQUEST)

    Wishlist.objects.create(user=user, product=product)
    return Response({'detail': 'Product added to wishlist successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    try:
        wishlist_item = Wishlist.objects.get(user=user, product=product)
        wishlist_item.delete()
        return Response({'detail': 'Product removed from wishlist successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({'detail': 'This product is not in your wishlist.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    products = [item.product for item in wishlist_items]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)