from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter

from .models import Order, OrderProduct, Product, ProductCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "stock", "created_at", "updated_at")
    list_filter = (
        ("price", NumericRangeFilter),
        ("stock", NumericRangeFilter),
    )
    search_fields = ("title",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "user"]
    list_filter = (
        ("date", DateRangeFilter),
        "user",
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderProduct._meta.get_fields()] + ["total_price"]

    list_filter = (
        ("quantity", NumericRangeFilter),
        "order__user",
        ("order__date", DateRangeFilter),
    )
    search_fields = ("product__title",)
    # exclude = ("price",)


@admin.register(ProductCategory)
class ProductCategoryAdmin(MPTTModelAdmin):
    list_display = ("title", "parent")
    search_fields = ("title",)
    mptt_level_indent = 20
    list_filter = ("parent",)
