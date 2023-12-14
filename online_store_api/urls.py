from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls"), name="accounts"),
    path("api/catalog/", include("catalog.urls"), name="catalog"),
    path("api/cms/", include("cms.urls"), name="cms"),
    path("api/blog/", include("blog.urls"), name="blog"),
    path("api/geo/", include("geo.urls"), name="geo"),
    path("api/localize/", include("localize.urls"), name="localize"),
    path("api/stores/", include("stores.urls"), name="stores"),
    path("ckeditor/", include("ckeditor_uploader.urls"), name="ckeditor_uploader"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.IS_SWAGGER_UI_ENABLED:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
    ]
