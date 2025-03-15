from rest_framework import serializers
from .models import Order, OrderItems, DeliveryOffice, Coupon
from ..customer.models import Customer


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"


class OrderCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone']


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)
    delivery_office = serializers.SerializerMethodField()
    user = OrderCustomerSerializer(source='user.profile')
    order_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'coupon', 'created_at',
                  'delivery_office', 'order_items', 'order_items_count', 'status', 'total', 'user']

    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        serializer = OrderItemsSerializer(order_items, many=True, context=self.context)
        return serializer.data

    def get_order_items_count(self, obj):
        # Counts the items in the order_items field
        return obj.order_items.count()
    def get_delivery_office(self, obj):
        # Assuming the delivery office model has `name` and `address` fields
        return f"{obj.delivery_office.name}, {obj.delivery_office.address}"


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryOffice
        fields = ["id", "office"]


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["id", 'code', 'percent', 'expire', 'count']
