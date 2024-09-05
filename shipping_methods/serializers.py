from rest_framework import serializers

from shipping_methods.models import ShippingMethod


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = [
            "id",
            "title",
            "provider",
            "description",
            "is_active",
            "min_price",
            "ship_price",
            "free_ship_over",
        ]
