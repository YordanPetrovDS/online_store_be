from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaxGroupViewSet

app_name = "taxes"

router = DefaultRouter()
router.register(r"tax-groups", TaxGroupViewSet, basename="taxgroup")

urlpatterns = [
    path("", include(router.urls)),
]
