from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, ValidationError

from online_store_api.main.models import Order, OrderProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "stock", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "date", "user"]


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ["id", "order", "product", "quantity"]

    def create(self, validate_data):
        product = get_object_or_404(Product, pk=validate_data["product"].id)

        try:
            quantity = int(validate_data["quantity"])
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")

        if quantity > product.stock:
            raise NotAcceptable("You order quantity more than the seller have")

        validate_data["price"] = product.price

        order_product = super().create(validate_data)
        order_product.save()
        return order_product

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result["price"] = instance.price
        result["total_price"] = instance.total_price()
        return result
