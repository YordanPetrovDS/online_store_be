from django.contrib import admin
from unfold.admin import ModelAdmin

from geo.models import Country, Region, State


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ("title", "code")
    search_fields = ("title", "code")


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ("title", "code", "region")
    search_fields = ("title", "code", "region__title")
    list_filter = ("region", "title")


@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display = ("title", "code", "country")
    search_fields = ("title", "code", "country__title")
    list_filter = ("country",)
