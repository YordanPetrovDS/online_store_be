from django.urls import include, path
from rest_framework import routers

from geo.views import CountryViewSet, RegionViewSet, StateViewSet

app_name = "geo"

router = routers.DefaultRouter()
router.register(r"regions", RegionViewSet, basename="regions")
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"states", StateViewSet, basename="states")

urlpatterns = [
    path("", include(router.urls)),
]
