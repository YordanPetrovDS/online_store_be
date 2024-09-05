from django.contrib import admin
from unfold.admin import ModelAdmin

from taxes.models import TaxGroup


@admin.register(TaxGroup)
class TaxGroupAdmin(ModelAdmin):
    list_display = ("title", "country", "percentage", "is_always_applied")
    search_fields = ("title", "country__title")
    list_filter = ("is_always_applied", "country")
