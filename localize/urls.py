from django.urls import include, path
from rest_framework import routers

from localize.views import CurrencyRateViewSet, CurrencyViewSet, LanguageViewSet

router = routers.DefaultRouter()
router.register(r"languages", LanguageViewSet, basename="languages")
router.register(r"currencies", CurrencyViewSet, basename="currencies")
router.register(r"currency-rates", CurrencyRateViewSet, basename="currency-rates")


urlpatterns = [
    path("", include(router.urls)),
]
