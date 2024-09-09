from rest_framework import viewsets

from orders.models import Order, OrderProduct, OrderStatus
from orders.serializers import (
    OrderProductSerializer,
    OrderSerializer,
    OrderStatusSerializer,
)


class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all().order_by("sort_order")
    serializer_class = OrderStatusSerializer
    lookup_field = "slug"


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-updated_at")
    serializer_class = OrderSerializer


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
