from django.contrib import admin

from geo.models import Country, Region, State


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("title", "code")
    search_fields = ("title", "code")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "region")
    search_fields = ("title", "code", "region__title")
    list_filter = ("region",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "country")
    search_fields = ("title", "code", "country__title")
    list_filter = ("country",)
