from django.contrib import admin

from accounts.models import UserAddress


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "state", "city", "address", "is_default")
    list_filter = ("country", "state", "city", "is_default")
    search_fields = ("user__username", "country__name", "state__name", "city", "address")
    raw_id_fields = ("user", "country", "state")
    list_editable = ("is_default",)
    ordering = ("country", "state", "city")
    fieldsets = ((None, {"fields": ("user", "country", "state", "city", "address", "is_default")}),)
