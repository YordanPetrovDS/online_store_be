import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from common.models import BaseModel

UserModel = get_user_model()


class AttributeType(models.TextChoices):
    OPTIONS = "options", _("Options")
    NUMBER = "number", _("Number")
    TEXT = "text", _("Text")


class PriceChangeType(models.TextChoices):
    REDUCE = "reduce", _("Reduce")
    INCREASE = "increase", _("Increase")
    REPLACE = "replace", _("Replace")


class Attribute(BaseModel):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=AttributeType.choices, default=AttributeType.TEXT)

    def __str__(self):
        return self.title


class AttributeOption(BaseModel):
    attribute = models.ForeignKey(Attribute, related_name="options", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["sort_order"]


class Product(BaseModel):
    TITLE_MAX_LENGTH = 100
    PRICE_MAX_DIGITS = 10
    PRICE_DECIMALS_PLACES = 2

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    price = models.DecimalField(max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DECIMALS_PLACES)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["id"]


class ProductAttribute(BaseModel):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    attribute = models.ForeignKey("Attribute", on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)
    value_number = models.FloatField(null=True, blank=True)
    value_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.attribute.title} for {self.product.name}"

    class Meta:
        ordering = ["id"]


class Order(BaseModel):
    date = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"id: {self.id} date: {self.date} - user: {self.user}"

    class Meta:
        ordering = ["id"]


class OrderProduct(BaseModel):
    PRICE_MAX_DIGITS = 10
    PRICE_DECIMALS_PLACES = 2

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMALS_PLACES,
    )

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"product: {self.product} - quantity: {self.quantity} - total price: {self.total_price()}"

    class Meta:
        ordering = ["id"]


class ProductCategory(BaseModel, MPTTModel):
    title = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    attributes = models.ManyToManyField(Attribute, related_name="categories", blank=True)

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.title


class ProductAttributeOption(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(AttributeOption, on_delete=models.CASCADE)
    price_change_type = models.CharField(
        max_length=10,
        choices=PriceChangeType.choices,
        default=None,
        null=True,
        blank=True,
    )
    price_change_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField()

    def clean(self):
        """
        Custom validation to ensure price_change_amount is zero when price_change_type is None.
        """

        price_change_types_values = [choice[0] for choice in PriceChangeType.choices]
        price_change_types_labels = ", ".join([choice[1] for choice in PriceChangeType.choices])

        if self.price_change_type is None and self.price_change_amount != 0:
            raise ValidationError("Price change amount must be zero when price change type is None.")
        elif self.price_change_type in price_change_types_values and self.price_change_amount <= 0:
            raise ValidationError(
                f"Price change amount must be non-zero when price change type is {price_change_types_labels}."
            )

    def save(self, *args, **kwargs):
        """
        Override the save method to include custom validation.
        """
        self.full_clean()
        super(ProductAttributeOption, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.option.title}"


class Brand(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
