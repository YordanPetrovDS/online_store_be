from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from utils.validators import image_validator


class SignPossitionType(models.TextChoices):
    BEFORE_PRICE = "before_price", _("Before price")
    AFTER_PRICE = "after_price", _("After price")


class Language(BaseModel):
    title = models.CharField(max_length=32)
    code = models.CharField(max_length=2, unique=True)
    icon = models.ImageField(
        upload_to=settings.LAGUAGES_ICONS_UPLOAD_PREFIX, blank=True, null=True, validators=[image_validator]
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Currency(BaseModel):
    title = models.CharField(max_length=32)
    code = models.CharField(max_length=3, unique=True)
    sign = models.CharField(max_length=8, unique=True)
    sign_possition = models.CharField(
        max_length=32, choices=SignPossitionType.choices, default=SignPossitionType.BEFORE_PRICE
    )

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.title


class CurrencyRate(BaseModel):
    currency_from = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="rates_from")
    currency_to = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="rates_to")
    rate = models.FloatField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.currency_from.title} -> {self.currency_to.title}: {self.rate}"
