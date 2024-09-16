from rest_framework import viewsets

from invoices.models import Invoice, InvoiceItem, InvoiceTotal
from invoices.serializers import (
    InvoiceItemSerializer,
    InvoiceSerializer,
    InvoiceTotalSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by("-id")
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all().order_by("sort_order")
    serializer_class = InvoiceItemSerializer


class InvoiceTotalViewSet(viewsets.ModelViewSet):
    queryset = InvoiceTotal.objects.all().order_by("sort_order")
    serializer_class = InvoiceTotalSerializer
