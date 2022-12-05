from posixpath import basename

from django.urls import include, path
from rest_framework import routers

from .views import OrderProductViewSet, OrderViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"order", OrderViewSet, basename="order")
router.register(r"order-product", OrderProductViewSet, basename="order-product")

urlpatterns = [
    path("", include(router.urls)),
]
