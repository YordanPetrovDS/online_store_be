from rest_framework import serializers

from invoices.models import Invoice, InvoiceItem, InvoiceStatus, InvoiceTotal


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

    def validate(self, data):
        if data["status"] == InvoiceStatus.ISSUED and not data.get("invoice_number"):
            raise serializers.ValidationError("Invoice number must be assigned when the status is issued.")
        return data


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = "__all__"


class InvoiceTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTotal
        fields = "__all__"
