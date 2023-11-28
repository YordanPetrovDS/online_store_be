from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from mptt.admin import MPTTModelAdmin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter

from catalog.models import (
    Attribute,
    AttributeOption,
    Brand,
    Order,
    OrderProduct,
    Product,
    ProductAttribute,
    ProductAttributeOption,
    ProductCategory,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "stock", "created_at", "updated_at")
    list_filter = (
        ("price", NumericRangeFilter),
        ("stock", NumericRangeFilter),
    )
    search_fields = ("title",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "user"]
    list_filter = (
        ("date", DateRangeFilter),
        "user",
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderProduct._meta.get_fields()] + ["total_price"]

    list_filter = (
        ("quantity", NumericRangeFilter),
        "order__user",
        ("order__date", DateRangeFilter),
    )
    search_fields = ("product__title",)
    # exclude = ("price",)


class ProductCategoryAttributesInline(admin.TabularInline):
    model = ProductCategory.attributes.through
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(MPTTModelAdmin):
    list_display = ("title", "parent", "display_attributes")
    search_fields = ("title",)
    mptt_level_indent = 20
    list_filter = ("parent",)
    inlines = [ProductCategoryAttributesInline]

    def display_attributes(self, obj):
        return ", ".join([attribute.title for attribute in obj.attributes.all()])

    display_attributes.short_description = "Attributes"


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ["title", "type"]


@admin.register(AttributeOption)
class AttributeOptionAdmin(admin.ModelAdmin):
    list_display = ("title", "attribute", "sort_order")
    list_filter = ("attribute",)
    search_fields = ("title",)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ("product", "attribute", "is_required", "value_number", "value_text")
    list_filter = ("product", "attribute", "is_required")
    search_fields = ("product__name", "attribute__title")


@admin.register(ProductAttributeOption)
class ProductAttributeOptionAdmin(admin.ModelAdmin):
    list_display = ["product", "option", "price_change_type", "price_change_amount", "stock"]
    list_filter = ["product", "option", "price_change_type"]
    search_fields = ["product__name", "option__title"]


@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    pass
