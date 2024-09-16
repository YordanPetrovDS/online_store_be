from django.contrib import admin
from unfold.admin import ModelAdmin

from invoices.models import Invoice, InvoiceItem, InvoiceStatus, InvoiceTotal


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ("id", "invoice_number", "status", "issued_date_time", "order", "customer")
    search_fields = ("invoice_number", "customer_first_name", "customer_last_name", "order__id")
    list_filter = ("status", "issued_date_time")
    readonly_fields = ("invoice_number", "issued_date_time")

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == InvoiceStatus.ISSUED:
            return self.readonly_fields + tuple([f.name for f in self.model._meta.fields if f.name != "status"])
        return self.readonly_fields


@admin.register(InvoiceItem)
class InvoiceItemAdmin(ModelAdmin):
    list_display = ("invoice", "title", "sku", "price", "quantity", "sort_order")
    search_fields = ("title", "sku")
    list_filter = ("invoice",)
    ordering = ("invoice", "sort_order")


@admin.register(InvoiceTotal)
class InvoiceTotalAdmin(ModelAdmin):
    list_display = ("invoice", "title", "type", "amount", "sort_order")
    search_fields = ("invoice__id", "title")
    list_filter = ("type",)
