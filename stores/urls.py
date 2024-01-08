from django.urls import include, path
from rest_framework import routers

from stores.views import StoreLocationViewSet, StoreSettingViewSet, StoreViewSet

router = routers.DefaultRouter()
router.register(r"stores", StoreViewSet, basename="stores")
router.register(r"store-locations", StoreLocationViewSet, basename="store_locations")
router.register(r"store-settings", StoreSettingViewSet, basename="store_settings")

urlpatterns = [
    path("", include(router.urls)),
]
