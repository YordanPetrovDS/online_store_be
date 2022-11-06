from django.urls import path
from knox import views as knox_views

from online_store_api.accounts.views import (
    ChangePasswordView,
    LoginView,
    RegisterView,
)

urlpatterns = (
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path(
        "api/change-password/",
        ChangePasswordView.as_view(),
        name="change password",
    ),
)
