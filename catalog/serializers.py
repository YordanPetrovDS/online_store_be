from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, ValidationError

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
    ProductMultimedia,
    Promotion,
)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["id", "title", "type"]


class AttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeOption
        fields = ["id", "attribute", "title", "sort_order"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "stock"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = "__all__"


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
            raise ValidationError("This order is not yours. Please enter your order id.")

        try:
            quantity = int(validate_data["quantity"])
        except Exception:
            raise ValidationError("Please Enter Your Quantity")

        if quantity > product.stock:
            raise NotAcceptable("You order quantity more than the seller have")

        validate_data["price"] = product.price

        order_product = super().create(validate_data)
        return order_product

    def update(self, instance, validate_data):
        product = get_object_or_404(Product, pk=validate_data["product"].id)
        order = get_object_or_404(Order, pk=validate_data["order"].id)

        try:
            quantity = int(validate_data["quantity"])
        except Exception:
            raise ValidationError("Please Enter Your Quantity")

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
            raise NotAcceptable("You order quantity more than the seller have")

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


class ProductCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ["id", "title", "parent", "children", "attributes"]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_children(self, obj):
        if obj.children.exists():
            return ProductCategorySerializer(obj.children.all(), many=True).data
        return []


class ProductAttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeOption
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = "__all__"


class ProductMultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMultimedia
        fields = ["id", "product", "image", "video"]


class ProductDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDocument
        fields = ["id", "product", "title", "file"]


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"
