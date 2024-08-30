from django.urls import path

from carts.views import AddProductToCartView, CartDetailView

app_name = "carts"

urlpatterns = [
    path("add-product/", AddProductToCartView.as_view(), name="add-product-to-cart"),
    path("<str:hash>/", CartDetailView.as_view(), name="cart-detail"),
]
