from django_filters import rest_framework as filters

from online_store_api.main.models import Order, OrderProduct, Product


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()
    stock = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ["price", "stock", "title"]


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
