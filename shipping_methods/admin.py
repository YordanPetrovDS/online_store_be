from django.contrib import admin
from unfold.admin import ModelAdmin

from shipping_methods.models import ShippingMethod


@admin.register(ShippingMethod)
class ShippingMethodAdmin(ModelAdmin):
    list_display = ("title", "provider", "is_active", "min_price", "ship_price", "free_ship_over")
    search_fields = ("title", "provider")
    list_filter = ("provider", "is_active")
    ordering = ("title", "min_price")
