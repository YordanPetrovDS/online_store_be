from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from geo.models import Country, State
from localize.models import Currency, Language
from utils.functions import get_upload_path
from utils.validators import image_validator


class Store(BaseModel):
    title = models.CharField(max_length=128)
    domain = models.CharField(max_length=128, unique=True)
    logo = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])
    default_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="stores")
    default_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="stores")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class StoreLocation(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(_("City"), max_length=64, blank=True)
    title = models.CharField(_("Title"), max_length=128)
    address = models.CharField(_("Address"), max_length=128, blank=True)
    phone = models.CharField(_("Phone"), max_length=64, blank=True)
    email = models.EmailField(_("Email"), max_length=64, blank=True)
    gps_latitude = models.FloatField(_("GPS Latitude"), null=True, blank=True)
    gps_longitude = models.FloatField(_("GPS Longitude"), null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])

    class Meta:
        ordering = ["id"]
        verbose_name = _("Store Location")
        verbose_name_plural = _("Store Locations")

    def __str__(self):
        return self.title


class StoreSetting(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="settings")
    title = models.CharField(_("Title"), max_length=128)
    slug = models.CharField(max_length=32, unique=True)
    value = models.CharField(max_length=128)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = _("Store Setting")
        verbose_name_plural = _("Store Settings")

    def __str__(self):
        return self.title
