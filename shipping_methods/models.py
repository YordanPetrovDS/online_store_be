from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from common.models import BaseModel


class ShippingMethodType(models.TextChoices):
    STANDARD = "standard", "Standard"
    ECONT = "econt", "Econt"
    SPEEDY = "speedy", "Speedy"


class ShippingMethod(BaseModel):
    title = models.CharField(max_length=64)
    provider = models.CharField(max_length=32, choices=ShippingMethodType.choices, default=ShippingMethodType.STANDARD)
    description = RichTextUploadingField(blank=True)
    is_active = models.BooleanField(default=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ship_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    free_ship_over = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title
