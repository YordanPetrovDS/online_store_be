from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from orders.models import OrderStatus
from utils.functions import get_upload_path
from utils.validators import image_validator


class ProviderTypes(models.TextChoices):
    BANK = "bank", _("Bank Transfer")
    COD = "cod", _("Cash on Delivery")
    PAYPAL = "paypal", _("PayPal")


class PaymentMethod(BaseModel):
    title = models.CharField(max_length=128)
    provider = models.CharField(max_length=32, choices=ProviderTypes.choices, default=ProviderTypes.BANK)
    description = models.CharField(max_length=1024)
    instructions = RichTextField()
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])
    is_active = models.BooleanField(default=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.title
