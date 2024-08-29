from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from localize.models import Currency, CurrencyRate, Language


@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    list_display = ("title", "code", "icon_link")

    def icon_link(self, obj):
        if obj.icon:
            return format_html('<a href="{}">Icon</a>', obj.icon.url)
        return "-"


@admin.register(Currency)
class CurrencyAdmin(ModelAdmin):
    list_display = ("title", "code", "sign", "sign_position")
    search_fields = ("title", "code", "sign")
    list_filter = ("sign_position",)


@admin.register(CurrencyRate)
class CurrencyRateAdmin(ModelAdmin):
    list_display = ("currency_from", "currency_to", "rate")
    list_select_related = ("currency_from", "currency_to")
    search_fields = ("currency_from__title", "currency_to__title", "rate")
    list_filter = ("currency_from", "currency_to")
