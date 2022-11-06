from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("online_store_api.accounts.urls")),
    path("api/", include("online_store_api.main.urls")),
]
