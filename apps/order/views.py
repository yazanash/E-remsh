import datetime

from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import OrderFilter
from .models import Order, OrderItems, Coupon, DeliveryOffice
from datetime import datetime, timezone

from .serializers import OrderSerializer, DeliverySerializer, CouponSerializer
from ..product.models import Product, ProductItems


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    filter_set = OrderFilter(request.GET, queryset=Order.objects.all().order_by('id'))
    res_page = 10  # items count per page
    paginator = PageNumberPagination()  # pagination
    paginator.page_size = res_page  # set items per page count
    query_set = paginator.paginate_queryset(filter_set.qs, request)
    serializer = OrderSerializer(query_set, many=True)
    current_page = paginator.page.number
    total_pages = paginator.page.paginator.num_pages
    next_page = current_page + 1 if current_page < total_pages else None
    previous_page = current_page - 1 if current_page > 1 else None
    return Response({
        "data": serializer.data,
        "current_page": current_page,
        "total_pages": total_pages,
        "next_page": next_page,
        "previous_page": previous_page
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_order_by_id(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    serializer = OrderSerializer(order, many=False, context={'request': request})
    return Response({"data":  serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_delivery_offices(request):
    delivery_offices = DeliveryOffice.objects.all()
    serializer = DeliverySerializer(delivery_offices, many=True)
    return Response({"offices": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = request.data["status"]
    order.save()
    serializer = OrderSerializer(order, many=False)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return Response({"message": "you don't have permission to delete this order "},
                        status=status.HTTP_403_FORBIDDEN)
    order.delete()
    return Response({"message": "order deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data
    order_items = data.get('order_items', [])

    if not order_items:
        return Response({"error": "no order received"}, status=status.HTTP_400_BAD_REQUEST)
    coupon = None
    if data['coupon'] is not None:
        try:
            coupon = Coupon.objects.get(code=data['coupon'])
        except Coupon.DoesNotExist:
            return Response({"error": "coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        if coupon.expire < datetime.now(timezone.utc) or coupon.count == 0:
            return Response({"error": "coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        previous_order = Order.objects.filter(user=user, coupon=coupon).exists()
        if previous_order:
            return Response({"error": "coupon has already been used by this user"}, status=status.HTTP_400_BAD_REQUEST)

    delivery_office = DeliveryOffice.objects.get(id=data['delivery_office'])
    if delivery_office is None:
        return Response({"error": "delivery office is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    order = Order.objects.create(
        user=user,
        delivery_office=delivery_office,
        coupon=coupon,
    )
    order_total = 0
    for item in order_items:
        try:
            product_item = ProductItems.objects.get(id=item['product'])
            product = product_item.product
        except Product.DoesNotExist:
            continue
        item_total = product.offer * item['quantity'] if product.offer != 0 else product.price * item['quantity']
        order_total += item_total
        OrderItems.objects.create(
            product=product,
            order=order,
            name=product.name,
            thumbnail=product.thumbnail,
            quantity=item['quantity'],
            color=product_item.color,
            size=product_item.size,
            price=product.price,
            offer=product.offer,
            has_offer=product.offer != 0,
            percent=int(product.offer / product.price) if product.price != 0 else 0,
            total=item_total
        )
    order.total = order_total
    if order.coupon is not None:
        order.total = order_total - (order_total * order.coupon.percent / 100)
    order.save()
    serializer = OrderSerializer(order, many=False,context={'request':request})
    return Response({"order": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_coupon(request):
    data = request.data
    serializer = CouponSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_coupon(request, coupon_id):
    data = request.data
    coupon = Coupon.objects.get(id=coupon_id)
    serializer = CouponSerializer(coupon, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_coupons(request):
    coupons = Coupon.objects.all()
    serializer = CouponSerializer(coupons, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_delivery(request):
    data = request.data
    serializer = DeliverySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_delivery(request, coupon_id):
    data = request.data
    delivery = DeliveryOffice.objects.get(id=coupon_id)
    serializer = DeliverySerializer(delivery, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deliveries(request):
    deliveries = DeliveryOffice.objects.all()
    serializer = DeliverySerializer(deliveries, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)



