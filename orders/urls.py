from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import (
    OrderProductViewSet,
    OrderQuoteViewSet,
    OrderStatusChangeViewSet,
    OrderStatusViewSet,
    OrderTotalViewSet,
    OrderViewSet,
)

app_name = "orders"

router = DefaultRouter()
router.register(r"order-status", OrderStatusViewSet, basename="order_status")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"order-products", OrderProductViewSet, basename="order_products")
router.register(r"order-quotes", OrderQuoteViewSet, basename="order_quotes")
router.register(r"order-status-changes", OrderStatusChangeViewSet, basename="order_status_changes")
router.register(r"order-totals", OrderTotalViewSet, basename="order_totals")

urlpatterns = [
    path("", include(router.urls)),
]
