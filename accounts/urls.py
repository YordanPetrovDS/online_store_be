from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import (
    LoginView,
    LogoutView,
    ProfileViewSet,
    RegisterView,
    UserAddressViewSet,
    UserReviewViewSet,
    UserWishlistViewSet,
)

app_name = "accounts"

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profiles")
router.register(r"user-addresses", UserAddressViewSet, basename="user-addresses")
router.register(r"user-wishlists", UserWishlistViewSet, basename="user-wishlists")
router.register(r"user-reviews", UserReviewViewSet, basename="user-reviews")

urlpatterns = (
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
)
