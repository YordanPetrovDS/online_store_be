from django.db.models import OuterRef, Subquery
from django_filters import rest_framework as filters

from catalog.models import Order, OrderProduct, Product, ProductAttributeOption


class ProductFilter(filters.FilterSet):
    price_from = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_to = filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = filters.BooleanFilter(method="filter_in_stock")
    brand = filters.BaseInFilter(field_name="brand__id")
    category = filters.BaseInFilter(field_name="categories__id")
    attribute_options = filters.CharFilter(method="filter_attribute_options")

    class Meta:
        model = Product
        fields = ["title"]

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)

    def filter_attribute_options(self, queryset, name, value):
        if not value:
            return queryset

        attribute_filters = value.split("|")
        subqueries = []

        for attr_filter in attribute_filters:
            attr_id, option_ids = attr_filter.split(":")
            option_ids = option_ids.split(",")

            # Create a subquery for each attribute and its options
            subquery = ProductAttributeOption.objects.filter(
                product_id=OuterRef("id"), option__attribute_id=attr_id, option_id__in=option_ids
            )

            subqueries.append(Subquery(subquery.values("id")[:1]))

        # Filter the queryset where each subquery has a result (i.e., a matching ProductAttributeOption)
        for subquery in subqueries:
            queryset = queryset.annotate(subquery_exists=Subquery(subquery)).filter(subquery_exists__isnull=False)

        return queryset.distinct()


class OrderFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ["date", "user"]


class OrderProductFilter(filters.FilterSet):
    quantity = filters.RangeFilter()
    price = filters.RangeFilter()

    class Meta:
        model = OrderProduct
        fields = ["quantity", "price"]
