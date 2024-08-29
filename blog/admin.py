from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin

from blog.models import Article, ArticleCategory, ArticleTag
from common.admin import IsActiveColumnMixin


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(IsActiveColumnMixin, SortableAdminMixin, TranslationAdmin, ModelAdmin):
    list_display = ("__str__", "is_active")
    list_per_page = 20


@admin.register(Article)
class ArticleAdmin(IsActiveColumnMixin, TranslationAdmin, ModelAdmin):
    list_display = (
        "slug",
        "title",
        "categories_titles",
        "is_active",
    )
    list_per_page = 20
    search_fields = ("slug", "title")

    def categories_titles(self, obj):
        return ", ".join([c.title for c in obj.categories.all()])


@admin.register(ArticleTag)
class ArticleTagAdmin(ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
