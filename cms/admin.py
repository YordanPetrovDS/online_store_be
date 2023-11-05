# Register your models here.
from adminsortable2.admin import (
    SortableAdminBase,
    SortableAdminMixin,
    SortableTabularInline,
)
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from cms.models import Banner, Page, Paragraph
from common.admin import IsActiveColumnMixin


class ParagraphStackedInline(TranslationStackedInline):
    model = Paragraph


class BannerTabularInline(SortableTabularInline):
    model = Banner


@admin.register(Page)
class PageAdmin(IsActiveColumnMixin, SortableAdminBase, TranslationAdmin):
    list_display = ("slug", "title", "is_published")
    list_per_page = 20
    search_fields = ("slug", "title")
    inlines = (ParagraphStackedInline, BannerTabularInline)


@admin.register(Banner)
class BannerAdmin(IsActiveColumnMixin, SortableAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "page", "is_active")
    list_per_page = 20
