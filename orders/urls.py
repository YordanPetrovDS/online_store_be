from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import OrderProductViewSet, OrderStatusViewSet, OrderViewSet

app_name = "orders"

router = DefaultRouter()
router.register(r"order-status", OrderStatusViewSet, basename="order_status")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"order-products", OrderProductViewSet, basename="order_products")

urlpatterns = [
    path("", include(router.urls)),
]
