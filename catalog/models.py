import datetime

from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel

UserModel = get_user_model()


class Product(BaseModel):
    TITLE_MAX_LENGTH = 100
    PRICE_MAX_DIGITS = 10
    PRICE_DECIMALS_PLACES = 2

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DECIMALS_PLACES
    )
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

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
