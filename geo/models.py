from django.db import models

from common.models import BaseModel


class Region(BaseModel):
    title = models.CharField(max_length=128)
    code = models.CharField(max_length=8, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Country(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="countries")
    title = models.CharField(max_length=128)
    code = models.CharField(max_length=2, unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.title


class State(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="states")
    title = models.CharField(max_length=128)
    code = models.CharField(max_length=2, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
