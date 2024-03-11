from django.contrib import admin
from django.utils.html import format_html

from localize.models import Currency, CurrencyRate, Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "icon_link")

    def icon_link(self, obj):
        if obj.image:
            return format_html('<a href="{}">Icon</a>', obj.image.url)
        return "-"


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "sign", "sign_position")
    search_fields = ("title", "code", "sign")
    list_filter = ("sign_position",)


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ("currency_from", "currency_to", "rate")
    list_select_related = ("currency_from", "currency_to")
    search_fields = ("currency_from__title", "currency_to__title", "rate")
    list_filter = ("currency_from", "currency_to")
