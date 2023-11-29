from django.db.models import CharField, F, Func, Sum, Value
from django.db.models.functions import Trim, TruncMonth
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.filters import (
    OrderFilter,
    OrderProductFilter,
    ProductFilter,
    PromotionFilter,
)
from catalog.models import (
    Attribute,
    AttributeOption,
    Brand,
    DiscountCode,
    Order,
    OrderProduct,
    Product,
    ProductAttribute,
    ProductAttributeOption,
    ProductCategory,
    ProductDocument,
    ProductMultimedia,
    Promotion,
)
from catalog.serializers import (
    AttributeOptionSerializer,
    AttributeSerializer,
    BrandSerializer,
    DiscountCodeSerializer,
    OrderProductSerializer,
    OrderSerializer,
    ProductAttributeOptionSerializer,
    ProductAttributeSerializer,
    ProductCategorySerializer,
    ProductDocumentSerializer,
    ProductMultimediaSerializer,
    ProductSerializer,
    PromotionSerializer,
)
from common.mixins import DefaultsMixin
from utils.validators import validate_query_param


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeOptionViewSet(viewsets.ModelViewSet):
    queryset = AttributeOption.objects.all()
    serializer_class = AttributeOptionSerializer


class ProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ("title",)


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


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

        query_params_list = ["date_start", "date_end", "metric"]
        metric_choices = ["price", "count"]
        metric = validate_query_param(query_params_list, request, metric_choices)[2]

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


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_fields = ["parent"]
    search_fields = ["title"]


class ProductAttributeOptionViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeOption.objects.all()
    serializer_class = ProductAttributeOptionSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class DiscountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer


class ProductMultimediaViewSet(viewsets.ModelViewSet):
    queryset = ProductMultimedia.objects.all()
    serializer_class = ProductMultimediaSerializer


class ProductDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProductDocument.objects.all()
    serializer_class = ProductDocumentSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    ilter_class = PromotionFilter
