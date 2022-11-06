from django_filters import rest_framework as filters
from rest_framework import status, viewsets

from online_store_api.main.models import Order, OrderProduct, Product
from online_store_api.main.serializers import (
    OrderProductSerializer,
    OrderSerializer,
    ProductSerializer,
)


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    price_flt = filters.NumericRangeFilter(field_name="price")

    class Meta:
        model = Product
        fields = ["price", "stock", "title"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = ProductFilter
    filterset_fields = ""


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderSerializer


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all().order_by("id")
    serializer_class = OrderProductSerializer
