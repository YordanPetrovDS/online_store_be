from django.contrib import admin

from online_store_api.main.models import Order, OrderProduct, Product


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    exclude = ("price",)
