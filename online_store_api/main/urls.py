from django.urls import include, path
from rest_framework import routers

from online_store_api.main.views import (
    OrderProductViewSet,
    OrderViewSet,
    ProductViewSet,
)

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet)
router.register(r"order", OrderViewSet)
router.register(r"order-product", OrderProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

import online_store_api.main.signals
