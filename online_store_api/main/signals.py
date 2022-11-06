from django.dispatch import receiver
from django.db.models import signals

from online_store_api.main.models import OrderProduct, Product


# @receiver(signals.post_save, sender=OrderProduct)
# def decrease_stock(instance, **kwargs):
#     product = Product.objects.get(id=instance.product.id)
#     product.stock -= instance.quantity
#     product.save()

# @receiver(signals.pre_save, sender=OrderProduct)
# def product_price(instance, **kwargs):
#     product = Product.objects.get(id=instance.product.id)
#     instance.price = product.price
#     instance.save()
