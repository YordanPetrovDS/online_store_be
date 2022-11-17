from calendar import month_name

from django_filters import rest_framework as filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters as drf_filters

from online_store_api.main.filters import (
    OrderFilter,
    OrderProductFilter,
    ProductFilter,
)
from online_store_api.main.models import Order, OrderProduct, Product
from online_store_api.main.serializers import (
    OrderProductSerializer,
    OrderSerializer,
    ProductSerializer,
)


class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering and pagination."""

    permission_classes = [permissions.IsAuthenticated]
    paginate_by = 25
    paginate_by_param = "page_size"
    max_paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)


class ProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ("title",)


class OrderViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderSerializer
    filter_backends = filters.DjangoFilterBackend
    filterset_class = OrderFilter

    @staticmethod
    def __sum_of_all_products_prices(products):
        return sum(product.total_price() for product in products)

    @action(methods=["get"], detail=False)
    def stats(self, request):
        metric_flt = {
            "count": len,
            "price": self.__sum_of_all_products_prices,
        }
        metric = request.query_params.get("metric", None)

        if not self.queryset:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "There are no any orders for this period."},
            )

        orders = {}
        result = []
        for order in self.queryset:
            ordered_products = order.orderproduct_set.all()
            month = f"{order.date.year} {month_name[order.date.month]}"
            if month not in orders:
                orders[month] = []
            orders[month] += [*ordered_products]

        for month in orders:
            value = metric_flt[metric](orders[month])
            result.append(
                {
                    "month": month,
                    "value": value,
                }
            )

        return Response(status=status.HTTP_200_OK, data=result)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "stats":
            date_start = self.request.query_params.get("date_start", None)
            date_end = self.request.query_params.get("date_end", None)
            queryset = queryset.filter(date__range=[date_start, date_end])
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class OrderProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all().order_by("id")
    serializer_class = OrderProductSerializer
    filter_backends = filters.DjangoFilterBackend
    filterset_class = OrderProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
