from django.db import models

from accounts.models import User, UserAddress
from carts.models import Cart
from catalog.models import Product
from common.models import BaseModel
from geo.models import Country
from localize.models import Currency
from shipping_methods.models import ShippingMethod
from taxes.models import TaxGroup


class OrderStatus(BaseModel):
    title = models.CharField(max_length=64)
    slug = models.CharField(max_length=64, unique=True)
    sort_order = models.PositiveIntegerField()

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Order Status"
        verbose_name_plural = "Order Statuses"

    def __str__(self):
        return self.title


class Order(BaseModel):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    user_agent = models.CharField(max_length=1024)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    is_invoice_requested = models.BooleanField(default=False)
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    customer_first_name = models.CharField(max_length=64)
    customer_last_name = models.CharField(max_length=64)
    customer_phone = models.CharField(max_length=64)
    customer_email = models.EmailField(max_length=64)
    customer_company_name = models.CharField(max_length=128, blank=True)
    customer_company_number = models.CharField(max_length=128, blank=True)
    customer_invoice_details = models.CharField(max_length=128, blank=True)
    billing_address = models.ForeignKey(
        UserAddress, null=True, blank=True, related_name="billing_address", on_delete=models.SET_NULL
    )
    billing_address_first_name = models.CharField(max_length=128, blank=True)
    billing_address_last_name = models.CharField(max_length=128, blank=True)
    billing_address_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL, related_name="billing_country"
    )
    billing_address_country_title = models.CharField(max_length=128, blank=True)
    billing_address_city = models.CharField(max_length=128, blank=True)
    billing_address_street = models.CharField(max_length=128, blank=True)
    billing_address_phone = models.CharField(max_length=128, blank=True)
    billing_address_email = models.EmailField(max_length=128, blank=True)
    billing_address_notes = models.TextField(blank=True)
    shipping_address = models.ForeignKey(
        UserAddress, null=True, blank=True, related_name="shipping_address", on_delete=models.SET_NULL
    )
    shipping_address_first_name = models.CharField(max_length=128, blank=True)
    shipping_address_last_name = models.CharField(max_length=128, blank=True)
    shipping_address_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL, related_name="shipping_country"
    )
    shipping_address_country_title = models.CharField(max_length=128, blank=True)
    shipping_address_city = models.CharField(max_length=128, blank=True)
    shipping_address_street = models.CharField(max_length=128, blank=True)
    shipping_address_phone = models.CharField(max_length=128, blank=True)
    shipping_address_email = models.EmailField(max_length=128, blank=True)
    shipping_address_notes = models.TextField(blank=True)
    payment_method = models.ForeignKey("payments_methods.PaymentMethod", on_delete=models.SET_NULL, null=True)
    payment_method_provider = models.CharField(max_length=32, blank=True)
    payment_method_title = models.CharField(max_length=128, blank=True)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    shipping_method_provider = models.CharField(max_length=32, blank=True)
    shipping_method_title = models.CharField(max_length=128, blank=True)
    shipping_method_track_number = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.pk} for {self.customer_first_name} {self.customer_last_name}"


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    tax_groups = models.ManyToManyField(TaxGroup, related_name="order_products")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_products")
    product_title = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=64)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"

    def save(self, *args, **kwargs):
        # Copy product details for historical record
        if not self.pk:
            self.product_title = self.product.title
            self.product_sku = self.product.sku
            self.product_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_title} ({self.quantity})"


class StatusType(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAIL = "fail", "Fail"


class OrderQuote(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_quotes")
    payment_method = models.ForeignKey(
        "payments_methods.PaymentMethod", on_delete=models.SET_NULL, null=True, related_name="order_quotes"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=512)
    expiration_date_time = models.DateTimeField(null=True, blank=True)
    transaction_date_time = models.DateTimeField(null=True, blank=True)
    transaction_number = models.CharField(max_length=128, blank=True)
    transaction_error = models.TextField(blank=True)
    status = models.CharField(max_length=7, choices=StatusType.choices, default=StatusType.PENDING)

    class Meta:
        verbose_name = "Order Quote"
        verbose_name_plural = "Order Quotes"

    def __str__(self):
        return f"Order Quote for {self.order} - {self.status}"


class OrderStatusChange(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_changes")
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="status_changes")
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="status_changes")
    notes = models.TextField()

    class Meta:
        verbose_name = "Order Status Change"
        verbose_name_plural = "Order Status Changes"
        ordering = ["-id"]

    def __str__(self):
        return (
            f"Order {self.order.pk} status changed to {self.status.title}"
            f" by {self.admin.username if self.admin else 'System'}"
        )


class OrderTotalType(models.TextChoices):
    SUBTOTAL = "subtotal", "Subtotal"
    TAX = "tax", "Tax"
    SHIPPING = "shipping", "Shipping"
    DISCOUNT = "discount", "Discount"
    TOTAL = "total", "Total"


class OrderTotal(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_totals")
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=OrderTotalType.choices, default=OrderTotalType.SUBTOTAL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sort_order = models.PositiveIntegerField()

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Order Total"
        verbose_name_plural = "Order Totals"

    def __str__(self):
        return f"{self.title} ({self.amount})"
