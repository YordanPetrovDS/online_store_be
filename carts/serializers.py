from rest_framework import serializers

from carts.models import (
    Cart,
    CartProduct,
    CartProductOption,
    Product,
    ProductAttributeOption,
)
from localize.models import Currency


class CartProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProductOption
        fields = ["id", "attribute_option", "attribute_option_title", "price_change_type", "price_change_amount"]


class CartProductSerializer(serializers.ModelSerializer):
    options = CartProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = CartProduct
        fields = ["id", "product", "product_title", "product_sku", "product_price", "quantity", "options"]


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "customer", "currency", "hash", "products"]


class AddProductToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    currency = serializers.CharField(required=False, allow_blank=True)
    hash = serializers.CharField(required=False, allow_blank=True)
    options = CartProductOptionSerializer(many=True, required=False)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user if self.context["request"].user.is_authenticated else None
        cart_hash = validated_data.get("hash")
        product_id = validated_data["product_id"]
        quantity = validated_data["quantity"]
        options_data = validated_data.get("options", [])
        currency = validated_data.get("currency")

        # Retrieve or create the Cart object
        if user:
            # For logged-in users
            cart, created = Cart.objects.get_or_create(customer=user, defaults={"currency": currency})
        else:
            # For guest users
            if cart_hash:
                cart = Cart.objects.filter(hash=cart_hash, customer__isnull=True).first()
                if not cart:
                    cart = Cart.objects.create(currency=Currency.objects.get(code="USD"))  # Default currency
            else:
                # Creating a new cart for guest users
                cart = Cart.objects.create(currency=Currency.objects.get(code="USD"))  # Default currency

        # Retrieve the Product object
        product = Product.objects.get(id=product_id)

        # Add or update the CartProduct
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "product_title": product.title,
                "product_sku": product.sku,
                "product_price": product.price,
                "quantity": quantity,
            },
        )
        if not created:
            cart_product.quantity += quantity
            cart_product.save()

        # Handle options if any
        for option_data in options_data:
            attribute_option = ProductAttributeOption.objects.get(id=option_data.get("attribute_option"))
            CartProductOption.objects.create(
                cart_product=cart_product,
                attribute_option=attribute_option,
                attribute_option_title=attribute_option.option.title,
                price_change_type=attribute_option.price_change_type,
                price_change_amount=attribute_option.price_change_amount,
            )

        return cart
