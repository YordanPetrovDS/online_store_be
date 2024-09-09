from django.contrib import admin
from unfold.admin import ModelAdmin

from orders.models import Order, OrderProduct, OrderStatus


@admin.register(OrderStatus)
class OrderStatusAdmin(ModelAdmin):
    list_display = ("title", "slug", "sort_order")
    search_fields = ("title", "slug")
    ordering = ("sort_order",)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "customer_first_name", "customer_last_name", "status", "updated_at")
    search_fields = ("customer_first_name", "customer_last_name", "customer_email")
    list_filter = ("status", "currency")


@admin.register(OrderProduct)
class OrderProductAdmin(ModelAdmin):
    list_display = ("order", "product_title", "product_sku", "product_price", "quantity")
    search_fields = ("product_title", "product_sku")
    list_filter = ("order", "product_title")
