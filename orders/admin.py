from django.contrib import admin
from unfold.admin import ModelAdmin

from orders.models import (
    Order,
    OrderProduct,
    OrderQuote,
    OrderStatus,
    OrderStatusChange,
    OrderTotal,
)


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


@admin.register(OrderQuote)
class OrderQuoteAdmin(ModelAdmin):
    list_display = ("order", "payment_method", "total", "status", "transaction_date_time")
    search_fields = ("order__id", "transaction_number", "payment_method__title")
    list_filter = ("status", "payment_method")


@admin.register(OrderStatusChange)
class OrderStatusChangeAdmin(ModelAdmin):
    list_display = ("order", "status", "admin", "notes")
    search_fields = ("order__id", "status__title", "admin__username")
    list_filter = ("status", "admin")


@admin.register(OrderTotal)
class OrderTotalAdmin(ModelAdmin):
    list_display = ("order", "title", "type", "amount", "sort_order")
    search_fields = ("order__id", "title")
    list_filter = ("type",)
