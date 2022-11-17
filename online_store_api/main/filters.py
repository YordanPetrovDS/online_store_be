from django_filters import rest_framework as filters

from online_store_api.main.models import Order, OrderProduct, Product


class ProductFilter(filters.FilterSet):
    price = filters.NumericRangeFilter()
    stock = filters.NumericRangeFilter()

    class Meta:
        model = Product
        fields = ["price", "stock", "title"]


class OrderFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ["date", "user"]


class OrderProductFilter(filters.FilterSet):
    quantity = filters.NumericRangeFilter()
    price = filters.NumericRangeFilter()

    class Meta:
        model = OrderProduct
        fields = ["quantity", "price"]
