import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from accounts.models import User
from cms.models import Page
from common.models import BaseModel, TinifiedImageField
from utils.validators import (
    document_validator,
    download_file_validator,
    image_validator,
    video_validator,
)

UserModel = get_user_model()


class AttributeType(models.TextChoices):
    OPTIONS = "options", _("Options")
    NUMBER = "number", _("Number")
    TEXT = "text", _("Text")


class PriceChangeType(models.TextChoices):
    REDUCE = "reduce", _("Reduce")
    INCREASE = "increase", _("Increase")
    REPLACE = "replace", _("Replace")


class DiscountType(models.TextChoices):
    AMOUNT = "amount", _("Amount")
    PERCENT = "percent", _("Percent")


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


class Brand(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ProductCategory(BaseModel, MPTTModel):
    title = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    attributes = models.ManyToManyField(Attribute, related_name="categories", blank=True)
    tax_groups = models.ManyToManyField("taxes.TaxGroup", related_name="categories", blank=True)

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.title


class Product(Page):
    PRICE_MAX_DIGITS = 10
    PRICE_DECIMALS_PLACES = 2

    base_price = models.DecimalField(max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DECIMALS_PLACES)
    price = models.DecimalField(max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DECIMALS_PLACES)
    stock = models.IntegerField(default=0)
    description = RichTextUploadingField(blank=True)
    sku = models.CharField(max_length=128, unique=True, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    categories = models.ManyToManyField(ProductCategory, related_name="products", blank=True)
    tax_groups = models.ManyToManyField("taxes.TaxGroup", related_name="products", blank=True)

    class Meta:
        ordering = ["id"]


class ProductAttribute(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)
    value_number = models.FloatField(null=True, blank=True)
    value_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.attribute.title} for {self.product.title}"

    class Meta:
        ordering = ["id"]


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
        price_change_types_labels = ", ".join(str(choice[1]) for choice in PriceChangeType.choices)

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
        return f"{self.product.title} - {self.option.title}"


class Order(BaseModel):
    date = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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


class DiscountCode(BaseModel):
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    allowed_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discount_codes",
    )
    allowed_brands = models.ManyToManyField(Brand, blank=True, related_name="discount_codes")
    allowed_categories = models.ManyToManyField(ProductCategory, blank=True, related_name="discount_codes")
    allowed_products = models.ManyToManyField(Product, blank=True, related_name="discount_codes")
    used_for_orders = models.ManyToManyField(Order, blank=True, related_name="discount_codes")
    code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    discount_type = models.CharField(
        max_length=7,
        choices=DiscountType.choices,
        default=DiscountType.AMOUNT,
    )
    discount_value = models.PositiveIntegerField()
    max_uses = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.code

    def clean(self):
        if self.discount_type == "percent" and not (1 <= self.discount_value <= 100):
            raise ValidationError("For percent discounts, the value must be between 1 and 100.")

    def save(self, *args, **kwargs):
        """
        Override the save method to include custom validation.
        """
        self.full_clean()
        super(DiscountCode, self).save(*args, **kwargs)


class ProductMultimedia(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="multimedia")
    image = TinifiedImageField(
        upload_to=settings.PRODUCTS_IMAGES_UPLOAD_PREFIX,
        blank=True,
        null=True,
        validators=[image_validator],
    )
    video = models.FileField(
        upload_to=settings.PRODUCTS_VIDEOS_UPLOAD_PREFIX,
        blank=True,
        null=True,
        validators=[video_validator],
    )

    def __str__(self):
        return f"{self.product.title}"

    class Meta:
        ordering = ["id"]


class ProductDocument(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(_("Title"), max_length=128)
    file = models.FileField(upload_to=settings.PRODUCTS_DOCUMENTS_UPLOAD_PREFIX, validators=[document_validator])

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Promotion(BaseModel):
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    title = models.CharField(max_length=128)
    allowed_brands = models.ManyToManyField(Brand, blank=True, related_name="promotions")
    allowed_categories = models.ManyToManyField(ProductCategory, blank=True, related_name="promotions")
    allowed_products = models.ManyToManyField(Product, blank=True, related_name="promotions")
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["valid_from"]


class ProductDownload(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="downloads")
    title = models.CharField(max_length=128)
    file = models.FileField(upload_to=settings.PRODUCTS_DOWNLOADS_UPLOAD_PREFIX, validators=[download_file_validator])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]
