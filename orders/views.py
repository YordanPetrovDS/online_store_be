from rest_framework import viewsets

from orders.models import (
    Order,
    OrderProduct,
    OrderQuote,
    OrderStatus,
    OrderStatusChange,
    OrderTotal,
)
from orders.serializers import (
    OrderProductSerializer,
    OrderQuoteSerializer,
    OrderSerializer,
    OrderStatusChangeSerializer,
    OrderStatusSerializer,
    OrderTotalSerializer,
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


class OrderQuoteViewSet(viewsets.ModelViewSet):
    queryset = OrderQuote.objects.all()
    serializer_class = OrderQuoteSerializer


class OrderStatusChangeViewSet(viewsets.ModelViewSet):
    queryset = OrderStatusChange.objects.all().order_by("-id")
    serializer_class = OrderStatusChangeSerializer


class OrderTotalViewSet(viewsets.ModelViewSet):
    queryset = OrderTotal.objects.all().order_by("sort_order")
    serializer_class = OrderTotalSerializer
