from adminsortable2.admin import (
    SortableAdminBase,
    SortableAdminMixin,
    SortableTabularInline,
)
from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from cms.models import Banner, Page, Paragraph
from common.admin import IsActiveColumnMixin


class ParagraphStackedInline(TranslationStackedInline, StackedInline):
    model = Paragraph


class BannerTabularInline(SortableTabularInline, TabularInline):
    model = Banner


@admin.register(Page)
class PageAdmin(IsActiveColumnMixin, SortableAdminBase, TranslationAdmin, ModelAdmin):
    list_display = ("slug", "title", "is_published")
    list_per_page = 20
    search_fields = ("slug", "title")
    inlines = (ParagraphStackedInline, BannerTabularInline)


@admin.register(Banner)
class BannerAdmin(IsActiveColumnMixin, SortableAdminMixin, ModelAdmin):
    list_display = ("__str__", "page", "is_active")
    list_per_page = 20


@admin.register(Paragraph)
class ParagraphAdmin(ModelAdmin):
    list_display = ("page", "title", "content", "sort_order", "image_link")
    search_fields = ("title", "content")
    list_per_page = 20
    list_filter = ("page",)
    ordering = ("sort_order",)

    def image_link(self, obj):
        if obj.image:
            return format_html('<a href="{}">Image</a>', obj.image.url)
        return "-"
