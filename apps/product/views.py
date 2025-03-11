from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Product, Category, Like, WishList, ProductItems, Image
from .serializers import ProductSerializer, CategorySerializer, ProductItemSerializer, ProductImageSerializer
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.

@api_view(['GET'])
def get_products(request):
    """ Get All Products """
    filter_set = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    res_page = 10  # items count per page
    paginator = PageNumberPagination()  # pagination
    paginator.page_size = res_page  # set items per page count
    query_set = paginator.paginate_queryset(filter_set.qs, request)
    serializer = ProductSerializer(query_set, many=True, context={'request': request})
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_product_by_id(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product, many=False, context={'request': request})
    product_items = ProductItems.objects.filter(product=product)
    items_serializer = ProductItemSerializer(product_items, many=True)
    product_images = Image.objects.filter(product=product)
    images_serializer = ProductImageSerializer(product_images, many=True)
    return Response({"data": {"product_info": serializer.data,
                              "product_items": items_serializer.data,
                              "images": images_serializer.data}}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    print(categories)
    serializer = CategorySerializer(categories, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if Like.objects.filter(user=user, product=product).exists():
        return Response({'detail': 'You have already liked this product.'}, status=status.HTTP_400_BAD_REQUEST)

    Like.objects.create(user=user, product=product)
    return Response({'detail': 'Product liked successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if WishList.objects.filter(user=user, product=product).exists():
        return Response({'detail': 'This product is already in your wishlist.'}, status=status.HTTP_400_BAD_REQUEST)

    WishList.objects.create(user=user, product=product)
    return Response({'detail': 'Product added to wishlist successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    try:
        wishlist_item = WishList.objects.get(user=user, product=product)
        wishlist_item.delete()
        return Response({'detail': 'Product removed from wishlist successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except WishList.DoesNotExist:
        return Response({'detail': 'This product is not in your wishlist.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    user = request.user
    wishlist_items = WishList.objects.filter(user=user)
    products = [item.product for item in wishlist_items]
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data)
        res = ProductSerializer(product, many=False)
        return Response({"data": res.data}, status=status.HTTP_200_OK)
    else:
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        """
        Dynamically assign permissions based on the HTTP method.
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Require authentication for POST requests
        return [AllowAny()]  # Allow unrestricted access for GET requests

    def get(self, request):
        filter_set = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
        res_page = 10  # items count per page
        paginator = PageNumberPagination()  # pagination
        paginator.page_size = res_page  # set items per page count
        query_set = paginator.paginate_queryset(filter_set.qs, request)
        serializer = ProductSerializer(query_set, many=True, context={'request': request})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Handle product creation
        data = request.data
        serializer = ProductSerializer(data=data)
        category_id = data.get('category')
        category = Category.objects.get(id=category_id)
        if serializer.is_valid():
            product = serializer.save(category=category)
            res = ProductSerializer(product, many=False, context={'request': request})
            return Response({"data": res.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RefreshRefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract the existing refresh token from the request
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify and blacklist the old refresh token
            old_refresh = RefreshToken(refresh_token)
            old_refresh.blacklist()  # Requires token blacklisting to be enabled

            # Create a new refresh token
            new_refresh = RefreshToken.for_user(request.user)
            return Response({"refresh": str(new_refresh)}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"message": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)