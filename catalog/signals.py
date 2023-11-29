from random import choices
from string import ascii_uppercase

from django.db.models import signals
from django.dispatch import receiver

from .models import DiscountCode, OrderProduct, Product


def generate_discount_code(length: int = 6, char_set: str = ascii_uppercase) -> str:
    return "".join(choices(char_set, k=length))


@receiver(signals.post_save, sender=OrderProduct)
def decrease_stock(instance: OrderProduct, **kwargs):
    product = Product.objects.get(id=instance.product.id)
    product.stock -= instance.quantity
    product.save()


@receiver(signals.post_delete, sender=OrderProduct)
def increase_stock(instance: OrderProduct, **kwargs):
    product = Product.objects.get(id=instance.product.id)
    product.stock += instance.quantity
    product.save()


@receiver(signals.pre_save, sender=DiscountCode)
def set_new_discount_code(sender, instance: DiscountCode, *args, **kwargs):
    if not instance.code:
        instance.code = generate_discount_code()
        while DiscountCode.objects.filter(code=instance.code).exists():
            instance.code = generate_discount_code()
