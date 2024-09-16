from django.urls import include, path
from rest_framework.routers import DefaultRouter

from invoices.views import InvoiceItemViewSet, InvoiceTotalViewSet, InvoiceViewSet

app_name = "invoices"

router = DefaultRouter()
router.register(r"invoices", InvoiceViewSet, basename="invoices")
router.register(r"invoice-items", InvoiceItemViewSet, basename="invoice-items")
router.register(r"invoice-totals", InvoiceTotalViewSet, basename="invoice-totals")

urlpatterns = [
    path("", include(router.urls)),
]
