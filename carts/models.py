import uuid

from django.db import models

from accounts.models import User
from catalog.models import PriceChangeType, Product, ProductAttributeOption
from common.models import BaseModel
from localize.models import Currency


class Cart(BaseModel):
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    hash = models.CharField(max_length=16, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = uuid.uuid4().hex[:16]  # Generate a random 16-character hash
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cart {self.hash} for {'guest' if not self.customer else self.customer.username}"


class CartProduct(BaseModel):
    cart = models.ForeignKey(Cart, related_name="products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        # Copy product details for historical record
        if not self.pk:
            self.product_title = self.product.title
            self.product_sku = self.product.sku
            self.product_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_title} (x{self.quantity}) in cart {self.cart.hash}"


class CartProductOption(BaseModel):
    cart_product = models.ForeignKey(CartProduct, related_name="options", on_delete=models.CASCADE)
    attribute_option = models.ForeignKey(ProductAttributeOption, on_delete=models.CASCADE)
    attribute_option_title = models.CharField(max_length=255)
    price_change_type = models.CharField(max_length=10, choices=PriceChangeType.choices)
    price_change_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Copy data from ProductAttributeOption for historical record
        if not self.pk:
            self.attribute_option_title = self.attribute_option.option.title
            self.price_change_type = self.attribute_option.price_change_type
            self.price_change_amount = self.attribute_option.price_change_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attribute_option_title} ({self.price_change_type} {self.price_change_amount})"
