from rest_framework import status, viewsets

from online_store_api.main.models import Order, OrderProduct, Product
from online_store_api.main.serializers import (
    OrderProductSerializer,
    OrderSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderSerializer


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all().order_by("id")
    serializer_class = OrderProductSerializer
