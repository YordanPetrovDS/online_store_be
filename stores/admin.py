from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from stores.models import Store, StoreLocation, StoreSetting


@admin.register(Store)
class StoreAdmin(ModelAdmin):
    list_display = ("title", "domain", "default_language", "default_currency", "logo_link")
    search_fields = ("title", "domain")
    list_filter = ("default_language", "default_currency")

    def logo_link(self, obj):
        if obj.logo:
            return format_html('<a href="{}">Logo</a>', obj.logo.url)
        return "-"


@admin.register(StoreLocation)
class StoreLocationAdmin(ModelAdmin):
    list_display = ("title", "country", "state", "city", "address", "phone", "email", "image_link")
    search_fields = ("title", "address", "phone", "email", "city")
    list_filter = ("country", "state", "city")

    def image_link(self, obj):
        if obj.image:
            return format_html('<a href="{}">Logo</a>', obj.image.url)
        return "-"


@admin.register(StoreSetting)
class StoreSettingAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ("store", "title", "slug", "is_public")
    list_filter = ("store", "is_public")
    search_fields = ("title", "slug", "store__title")
