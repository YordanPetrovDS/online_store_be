from rest_framework import serializers

from taxes.models import TaxGroup


class TaxGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxGroup
        fields = ["id", "title", "country", "percentage", "is_always_applied"]
