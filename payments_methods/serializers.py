from rest_framework import serializers

from payments_methods.models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "title",
            "provider",
            "description",
            "instructions",
            "image",
            "is_active",
            "order_status",
        ]
