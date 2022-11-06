from django.contrib import admin

from online_store_api.main.models import Order, OrderProduct, Product
from rangefilter.filters import (
    DateRangeFilter,
    DateTimeRangeFilter,
    NumericRangeFilter,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = (
        ("price", NumericRangeFilter),
        ("stock", NumericRangeFilter),
    )
    search_fields = ("title",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = (
        ("date", DateRangeFilter),
        "user",
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    exclude = ("price",)
