from django.urls import include, path
from rest_framework.routers import DefaultRouter

from newsletter.views import SubscriberViewSet

router = DefaultRouter()
router.register(r"subscribers", SubscriberViewSet, basename="subscribers")


urlpatterns = [
    path("", include(router.urls)),
]
