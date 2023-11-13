from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from .models import Order, OrderProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "stock"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "date"]

    def create(self, validate_data):
        validate_data["user"] = self.context["request"].user
        order = super().create(validate_data)
        order.save()
        return order


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ["id", "order", "product", "quantity"]

    def create(self, validate_data):
        product = get_object_or_404(Product, pk=validate_data["product"].id)
        order = get_object_or_404(Order, pk=validate_data["order"].id)

        if self.context["request"].user.id != order.user.id:
            raise serializers.ValidationError(detail={"Error": "This order is not yours. Please enter your order id."})

        try:
            quantity = int(validate_data["quantity"])
        except Exception:
            raise serializers.ValidationError(detail={"Error": "Please Enter Your Quantity"})

        if quantity > product.stock:
            raise NotAcceptable(detail={"Error": "You order quantity more than the seller have"})

        validate_data["price"] = product.price

        order_product = super().create(validate_data)
        return order_product

    def update(self, instance, validate_data):
        product = get_object_or_404(Product, pk=validate_data["product"].id)
        order = get_object_or_404(Order, pk=validate_data["order"].id)

        try:
            quantity = int(validate_data["quantity"])
        except Exception:
            raise serializers.ValidationError(detail={"Error": "Please Enter Your Quantity"})

        if validate_data["product"] != instance.product:
            product_old: Product = instance.product
            product_old.stock += instance.quantity
            product_old.save()
            instance.price = product.price
            instance.product = product
        else:
            product.stock += instance.quantity
            product.save()

        if quantity > product.stock:
            raise NotAcceptable(detail={"Error": "You order quantity more than the seller have"})

        instance.quantity = quantity
        instance.order = order
        instance.save()
        return instance

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result["price"] = instance.price
        result["total_price"] = instance.total_price()
        result["order_date"] = instance.order.date
        result["product_name"] = instance.product.title
        return result
