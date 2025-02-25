from rest_framework import serializers
from .models import Order, OrderItems, DeliveryOffice


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        serializer = OrderItemsSerializer(order_items, many=True)
        return serializer.data


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryOffice
        fields = ["id", "office"]
