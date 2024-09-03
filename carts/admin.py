from django.contrib import admin
from unfold.admin import ModelAdmin

from carts.models import Cart, CartProduct, CartProductOption


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ("id", "customer", "currency", "hash")
    search_fields = ("hash",)
    list_filter = ("customer", "currency")


@admin.register(CartProduct)
class CartProductAdmin(ModelAdmin):
    list_display = ("id", "cart", "product_title", "product_sku", "product_price", "quantity")
    search_fields = ("product_title", "product_sku")
    list_filter = ("cart",)


@admin.register(CartProductOption)
class CartProductOptionAdmin(ModelAdmin):
    list_display = ("id", "cart_product", "attribute_option_title", "price_change_type", "price_change_amount")
    search_fields = ("attribute_option_title",)
    list_filter = ("price_change_type",)
