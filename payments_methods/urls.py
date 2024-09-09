from django.urls import include, path
from rest_framework.routers import DefaultRouter

from payments_methods.views import PaymentMethodViewSet

app_name = "payment_methods"

router = DefaultRouter()
router.register(r"payment-methods", PaymentMethodViewSet, basename="payment_methods")

urlpatterns = [
    path("", include(router.urls)),
]
