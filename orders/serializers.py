from rest_framework import serializers

from orders.models import (
    Order,
    OrderProduct,
    OrderQuote,
    OrderStatus,
    OrderStatusChange,
    OrderTotal,
)


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ["id", "title", "slug", "sort_order"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderQuote
        fields = "__all__"


class OrderStatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusChange
        fields = "__all__"


class OrderTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTotal
        fields = "__all__"
