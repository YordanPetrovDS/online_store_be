from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from payments_methods.models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ("title", "provider", "is_active", "order_status", "icon_link")
    search_fields = ("title", "provider")
    list_filter = ("provider", "is_active")

    def icon_link(self, obj: PaymentMethod):
        if obj.image:
            return format_html('<a href="{}">Image</a>', obj.image.url)
        return "-"
