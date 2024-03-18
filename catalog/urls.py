from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import (
    AttributeOptionViewSet,
    AttributeViewSet,
    BrandViewSet,
    DiscountCodeViewSet,
    OrderProductViewSet,
    OrderViewSet,
    ProductAttributeOptionViewSet,
    ProductAttributeViewSet,
    ProductCategoryViewSet,
    ProductDocumentViewSet,
    ProductDownloadViewSet,
    ProductMultimediaViewSet,
    ProductViewSet,
    PromotionViewSet,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"order-product", OrderProductViewSet, basename="order-product")
router.register(r"product-categories", ProductCategoryViewSet, basename="product-categories")
router.register(r"attributes", AttributeViewSet, basename="attributes")
router.register(r"attribute-options", AttributeOptionViewSet, basename="attribute-options")
router.register(r"product-attributes", ProductAttributeViewSet, basename="product-attributes")
router.register(r"product-attribute-options", ProductAttributeOptionViewSet, basename="product-attribute-options")
router.register(r"brands", BrandViewSet, basename="brands")
router.register(r"discount-codes", DiscountCodeViewSet, basename="discount-codes")
router.register(r"product-multimedia", ProductMultimediaViewSet, basename="product-multimedia")
router.register(r"product-documents", ProductDocumentViewSet, basename="product-documents")
router.register(r"promotions", PromotionViewSet, basename="promotions")
router.register(r"product-downloads", ProductDownloadViewSet, basename="product-downloads")

urlpatterns = [
    path("", include(router.urls)),
]
