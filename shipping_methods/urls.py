from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shipping_methods.views import ShippingMethodViewSet

app_name = "shipping_methods"

router = DefaultRouter()
router.register(r"shipping-methods", ShippingMethodViewSet, basename="shipping_methods")

urlpatterns = [
    path("", include(router.urls)),
]
