from django.urls import include, path
from rest_framework import routers

from catalog.views import (
    OrderProductViewSet,
    OrderViewSet,
    ProductCategoryViewSet,
    ProductViewSet,
)

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"order", OrderViewSet, basename="order")
router.register(r"order-product", OrderProductViewSet, basename="order-product")
router.register(r"categories", ProductCategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
