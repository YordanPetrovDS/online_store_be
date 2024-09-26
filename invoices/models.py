from django.db import models
from django.utils import timezone

from accounts.models import User, UserAddress
from catalog.models import Product
from common.models import BaseModel
from geo.models import Country
from localize.models import Currency
from orders.models import Order
from payments_methods.models import PaymentMethod


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ISSUED = "issued", "Issued"
    REVOKED = "revoked", "Revoked"


class Invoice(BaseModel):
    status = models.CharField(max_length=8, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    issued_date_time = models.DateTimeField(null=True, blank=True)
    invoice_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="invoices")
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name="invoices")
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="invoices")
    customer_first_name = models.CharField(max_length=64)
    customer_last_name = models.CharField(max_length=64)
    customer_phone = models.CharField(max_length=64)
    customer_email = models.EmailField(max_length=64)
    customer_company_name = models.CharField(max_length=128, blank=True)
    customer_company_number = models.CharField(max_length=128, blank=True)
    customer_invoice_details = models.CharField(max_length=128, blank=True)
    billing_address = models.ForeignKey(
        UserAddress, null=True, blank=True, on_delete=models.SET_NULL, related_name="billing_address_invoice"
    )
    billing_address_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL, related_name="billing_country_invoice"
    )
    billing_address_country_title = models.CharField(max_length=128, blank=True)
    billing_address_city = models.CharField(max_length=128, blank=True)
    billing_address_street = models.CharField(max_length=128, blank=True)
    billing_address_phone = models.CharField(max_length=128, blank=True)
    billing_address_email = models.EmailField(max_length=128, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, related_name="invoices")
    payment_method_provider = models.CharField(max_length=32, blank=True)
    payment_method_title = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        # Auto-assign invoice_number when status is changed to "issued"
        if self.status == InvoiceStatus.ISSUED and self.invoice_number is None:
            highest_invoice_number = Invoice.objects.filter(status=InvoiceStatus.ISSUED).aggregate(
                models.Max("invoice_number")
            )["invoice_number__max"]
            self.invoice_number = (highest_invoice_number or 0) + 1
            self.issued_date_time = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Invoice #{self.invoice_number or "Draft"} for Order {self.order.pk}'


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="invoice_items")
    title = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    sort_order = models.PositiveIntegerField()

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"

    def __str__(self):
        return f"{self.title} (x{self.quantity}) - {self.price} each"


class InvoiceTotalType(models.TextChoices):
    SUBTOTAL = "subtotal", "Subtotal"
    TAX = "tax", "Tax"
    SHIPPING = "shipping", "Shipping"
    DISCOUNT = "discount", "Discount"
    TOTAL = "total", "Total"


class InvoiceTotal(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_totals")
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=InvoiceTotalType.choices, default=InvoiceTotalType.SUBTOTAL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sort_order = models.PositiveIntegerField()

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Invoice Total"
        verbose_name_plural = "Invoice Totals"

    def __str__(self):
        return f"{self.title} - {self.amount}"
