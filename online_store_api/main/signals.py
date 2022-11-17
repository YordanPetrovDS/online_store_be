from django.db.models import signals
from django.dispatch import receiver

from online_store_api.main.models import OrderProduct, Product


@receiver(signals.post_save, sender=OrderProduct)
def decrease_stock(instance, created, **kwargs):
    if created:
        product = Product.objects.get(id=instance.product.id)
        product.stock -= instance.quantity
        product.save()
