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
    hash = serializers.CharField(required=False, allow_blank=True)
    options = CartProductOptionSerializer(many=True, required=False)
    currency_code = serializers.CharField(max_length=3)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value

    def validate_currency_code(self, value):
        if value and not Currency.objects.filter(code=value).exists():
            raise serializers.ValidationError("Invalid currency code.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user if self.context["request"].user.is_authenticated else None
        cart_hash = validated_data.get("hash")
        product_id = validated_data["product_id"]
        quantity = validated_data["quantity"]
        options_data = validated_data.get("options", [])
        currency_code = validated_data.get("currency_code")

        # Determine the currency based on the provided currency code
        currency = Currency.objects.get(code=currency_code)

        # Retrieve or create the Cart object
        if user:
            # For logged-in users
            cart, _ = Cart.objects.get_or_create(customer=user, defaults={"currency": currency})
        else:
            # For guest users
            if cart_hash:
                cart = Cart.objects.filter(hash=cart_hash, customer__isnull=True).first()
                if not cart:
                    cart = Cart.objects.create(currency=currency)
            else:
                # Creating a new cart for guest users
                cart = Cart.objects.create(currency=currency)

        # Retrieve the Product object
        product = Product.objects.get(id=product_id)

        # Get or Create the CartProduct
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

        # Update the quantity if the CartProduct already exists
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


class ModifyCartSerializer(serializers.Serializer):
    hash = serializers.CharField(required=False, allow_blank=True)
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(required=False, min_value=0)
    currency_code = serializers.CharField(required=False, max_length=3)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value

    def validate_currency_code(self, value):
        if value and not Currency.objects.filter(code=value).exists():
            raise serializers.ValidationError("Invalid currency code.")
        return value

    def update_cart(self, user):
        hash = self.validated_data.get("hash")
        product_id = self.validated_data.get("product_id")
        quantity = self.validated_data.get("quantity")
        currency_code = self.validated_data.get("currency_code")

        # Determine the currency based on the provided currency code
        currency = Currency.objects.get(code=currency_code)

        if user.is_authenticated:
            # Retrieve or create cart for authenticated users
            cart, _ = Cart.objects.get_or_create(customer=user, defaults={"currency": currency})
        else:
            # Handle guest user carts based on the hash
            cart = Cart.objects.filter(hash=hash, customer__isnull=True).first()
            if not cart:
                cart = cart = Cart.objects.create(currency=currency)

        # Retrieve the Product
        product = Product.objects.get(id=product_id)
        # Get or create the CartProduct
        cart_product, _ = CartProduct.objects.get_or_create(cart=cart, product=product)

        # Update the quantity or delete the CartProduct
        if quantity == 0:
            cart_product.delete()
        else:
            cart_product.quantity = quantity
            cart_product.save()

        return cart
