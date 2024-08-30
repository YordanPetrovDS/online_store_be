from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("api/catalog/", include(("catalog.urls", "catalog"), namespace="catalog")),
    path("api/cms/", include(("cms.urls", "cms"), namespace="cms")),
    path("api/blog/", include(("blog.urls", "blog"), namespace="blog")),
    path("api/geo/", include(("geo.urls", "geo"), namespace="geo")),
    path("api/localize/", include(("localize.urls", "localize"), namespace="localize")),
    path("api/stores/", include(("stores.urls", "stores"), namespace="stores")),
    path("api/newsletter/", include(("newsletter.urls", "newsletter"), namespace="newsletter")),
    path("api/carts/", include(("carts.urls", "carts"), namespace="carts")),
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
