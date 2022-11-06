from django.urls import path

from online_store_api.accounts.views import LoginView, LogoutView, RegisterView

urlpatterns = (
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
)

import online_store_api.accounts.signals
