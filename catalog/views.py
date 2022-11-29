from django.db.models import CharField, F, Func, Sum, Value
from django.db.models.functions import Trim, TruncMonth
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.mixins import DefaultsMixin
from common.validators import validate_query_param
from .filters import OrderFilter, OrderProductFilter, ProductFilter
from .models import Order, OrderProduct, Product
from .serializers import (
    OrderProductSerializer,
    OrderSerializer,
    ProductSerializer,
)


class ProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ("title",)


class OrderViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    @action(methods=["get"], detail=False)
    def stats(self, request):
        metric_flt = {
            "count": F("orderproduct__quantity"),
            "price": F("orderproduct__price") * F("orderproduct__quantity"),
        }

        date_start, date_end, metric = (
            validate_query_param("date_start", request),
            validate_query_param("date_end", request),
            validate_query_param("metric", request, ["price", "count"]),
        )

        orders_queryset = self.get_queryset()

        if not orders_queryset:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "There are no any orders for this period."},
            )

        orders_queryset = (
            orders_queryset.annotate(
                month_date=TruncMonth("date"),
                month=Trim(
                    Func(
                        F("date"),
                        Value("YYYY Month"),
                        arity=2,
                        function="to_char",
                        output_field=CharField(),
                    )
                ),
            )
            .values("month")
            .annotate(value=Sum(metric_flt[metric]))
            .order_by("month_date")
        )

        page = self.paginate_queryset(orders_queryset)
        return self.get_paginated_response(page)

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


class OrderProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
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
