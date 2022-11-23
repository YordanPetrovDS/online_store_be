from calendar import month_name
from datetime import datetime

from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

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
    filter_backends = (filters.DjangoFilterBackend,)
    paginate_by = 5
    paginate_by_param = "page_size"
    max_paginate_by = 100


class ProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ("title",)


class OrderViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    @action(methods=["get"], detail=False)
    def stats(self, request):
        metric_flt = {
            "count": lambda x: sum(el.quantity for el in x),
            "price": lambda x: sum(el.total_price() for el in x),
        }
        try:
            date_start, date_end, metric = (
                request.query_params["date_start"],
                request.query_params["date_end"],
                request.query_params["metric"],
            )
        except Exception:
            raise serializers.ValidationError(
                detail={
                    "Error": "There is/are missing filter field/s - required filter fields are 'date_start', 'date_end' and 'metric'"
                }
            )
        if metric not in ["price", "count"]:
            raise serializers.ValidationError(
                detail={
                    "Error": "Incorrect value for filter field 'metric', the value should be one of 'count' or 'price'"
                },
            )

        orders_queryset = self.get_queryset()

        if not orders_queryset:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "There are no any orders for this period."},
            )

        orders_per_month = {}
        result = []
        for order in orders_queryset:
            ordered_products = order.orderproduct_set.all()
            month = f"{order.date.year} {month_name[order.date.month]}"
            if month not in orders_per_month:
                orders_per_month[month] = []
            orders_per_month[month] += [*ordered_products]

        orders_per_month = dict(
            sorted(
                orders_per_month.items(),
                key=lambda x: datetime.strptime(x[0], "%Y %B"),
            )
        )

        for month in orders_per_month:
            value = metric_flt[metric](orders_per_month[month])
            result.append(
                {
                    "month": month,
                    "value": value,
                }
            )

        return Response(status=status.HTTP_200_OK, data=result)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["list", "stats"]:
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user.id)
            if self.action == "stats":
                date_start = self.request.query_params.get("date_start", None)
                date_end = self.request.query_params.get("date_end", None)
                queryset = queryset.filter(date__range=[date_start, date_end])
        return queryset

    def get_object(self):
        the_object = super().get_object()
        if the_object.user != self.request.user and (
            not self.request.user.is_staff or self.action != "retrieve"
        ):
            raise PermissionDenied
        return the_object


class OrderProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all().order_by("id")
    serializer_class = OrderProductSerializer
    filterset_class = OrderProductFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"message": "Instance is successfully deleted"},
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list" and not self.request.user.is_staff:
            queryset = queryset.filter(order__user=self.request.user)
        return queryset

    def get_object(self):
        the_object = super().get_object()
        if the_object.order.user != self.request.user and (
            not self.request.user.is_staff or self.action != "retrieve"
        ):
            raise PermissionDenied
        return the_object
