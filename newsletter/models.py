from django.db import models

from common.models import BaseModel


class Subscriber(BaseModel):
    email = models.EmailField(max_length=128, unique=True)
    is_email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email
