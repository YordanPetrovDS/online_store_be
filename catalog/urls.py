from django.urls import include, path
from rest_framework import routers

from catalog.views import (
    AttributeOptionViewSet,
    AttributeViewSet,
    BrandViewSet,
    OrderProductViewSet,
    OrderViewSet,
    ProductAttributeOptionViewSet,
    ProductAttributeViewSet,
    ProductCategoryViewSet,
    ProductViewSet,
)

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"order", OrderViewSet, basename="order")
router.register(r"order-product", OrderProductViewSet, basename="order-product")
router.register(r"product-categories", ProductCategoryViewSet, basename="product-categories")
router.register(r"attributes", AttributeViewSet, basename="attributes")
router.register(r"attribute-options", AttributeOptionViewSet, basename="attribute-options")
router.register(r"product-attributes", ProductAttributeViewSet, basename="product-attributes")
router.register(r"product-attribute-options", ProductAttributeOptionViewSet, basename="product-attribute-options")
router.register(r"brands", BrandViewSet, basename="brands")

urlpatterns = [
    path("", include(router.urls)),
]
