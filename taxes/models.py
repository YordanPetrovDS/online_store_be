from django.db import models

from common.models import BaseModel


class TaxGroup(BaseModel):
    title = models.CharField(max_length=128)
    country = models.ForeignKey("geo.Country", on_delete=models.CASCADE, related_name="tax_groups")
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_always_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.title
