from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from mptt.admin import MPTTModelAdmin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter
from unfold.admin import ModelAdmin

from catalog.models import (
    Attribute,
    AttributeOption,
    Brand,
    DiscountCode,
    Order,
    OrderProduct,
    Product,
    ProductAttribute,
    ProductAttributeOption,
    ProductCategory,
    ProductDocument,
    ProductDownload,
    ProductMultimedia,
    Promotion,
)


class ValidityFilter(admin.SimpleListFilter):
    title = "Validity"
    parameter_name = "validity"

    def lookups(self, request, model_admin):
        return (
            ("valid", "Currently Valid"),
            ("expired", "Expired"),
        )

    def queryset(self, request, queryset):
        if self.value() == "valid":
            return queryset.filter(valid_from__lte=timezone.now(), valid_until__gte=timezone.now())
        if self.value() == "expired":
            return queryset.filter(valid_until__lt=timezone.now())


class ProductListFilter(admin.SimpleListFilter):
    title = _("product")
    parameter_name = "product"

    def lookups(self, request, model_admin):
        products = Product.objects.all()
        return [(product.id, product.title) for product in products]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(product__id=self.value())
        return queryset


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("title", "price", "stock", "created_at", "updated_at")
    list_filter = (
        ("price", NumericRangeFilter),
        ("stock", NumericRangeFilter),
    )
    search_fields = ("title",)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["id", "date", "user"]
    list_filter = (
        ("date", DateRangeFilter),
        "user",
    )


@admin.register(OrderProduct)
class OrderProductAdmin(ModelAdmin):
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
class ProductCategoryAdmin(MPTTModelAdmin, ModelAdmin):
    list_display = ("title", "parent", "display_attributes")
    search_fields = ("title",)
    mptt_level_indent = 20
    list_filter = ("parent",)
    inlines = [ProductCategoryAttributesInline]

    def display_attributes(self, obj):
        return ", ".join([attribute.title for attribute in obj.attributes.all()])

    display_attributes.short_description = "Attributes"


@admin.register(Attribute)
class AttributeAdmin(ModelAdmin):
    list_display = ["title", "type"]


@admin.register(AttributeOption)
class AttributeOptionAdmin(ModelAdmin):
    list_display = ("title", "attribute", "sort_order")
    list_filter = ("attribute",)
    search_fields = ("title",)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ModelAdmin):
    list_display = ("product", "attribute", "is_required", "value_number", "value_text")
    list_filter = ("product", "attribute", "is_required")
    search_fields = ("product__name", "attribute__title")


@admin.register(ProductAttributeOption)
class ProductAttributeOptionAdmin(ModelAdmin):
    list_display = ["product", "option", "price_change_type", "price_change_amount", "stock"]
    list_filter = ["product", "option", "price_change_type"]
    search_fields = ["product__name", "option__title"]


@admin.register(Brand)
class BrandAdmin(TranslationAdmin, ModelAdmin):
    pass


@admin.register(DiscountCode)
class DiscountCodeAdmin(ModelAdmin):
    list_display = ["code", "discount_type", "discount_value", "valid_from", "valid_until", "allowed_user"]
    list_filter = (
        "discount_type",
        "allowed_user",
        ValidityFilter,
        "allowed_brands",
        "allowed_categories",
        "allowed_products",
    )


@admin.register(ProductMultimedia)
class ProductMultimediaAdmin(ModelAdmin):
    list_display = ("product", "image_link", "video_link")

    def image_link(self, obj):
        if obj.image:
            return format_html('<a href="{}">Image</a>', obj.image.url)
        return "-"

    image_link.short_description = "Image"

    def video_link(self, obj):
        if obj.video:
            return format_html('<a href="{}">Video</a>', obj.video.url)
        return "-"

    video_link.short_description = "Video"


@admin.register(ProductDocument)
class ProductDocumentAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ("title", "product", "file_link")
    search_fields = ("title", "product__title")
    list_filter = (ProductListFilter,)

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}">File</a>', obj.file.url)
        return "-"

    file_link.short_description = "File"


@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display = ("title", "valid_from", "valid_until", "discount_percent")
    list_filter = ("valid_from", "valid_until", "discount_percent", ValidityFilter)
    search_fields = ("title",)


@admin.register(ProductDownload)
class ProductDownloadAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ("title", "product", "file_link")
    search_fields = ("title", "product__name")
    list_filter = (ProductListFilter,)

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}">File</a>', obj.file.url)
        return "-"

    file_link.short_description = "File"
