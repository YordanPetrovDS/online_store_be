from django.urls import path

from carts.views import AddProductToCartView, CartDetailView, ModifyCartView

app_name = "carts"

urlpatterns = [
    path("add-product/", AddProductToCartView.as_view(), name="add-product-to-cart"),
    path("modify-cart/", ModifyCartView.as_view(), name="modify-cart"),
    path("<str:hash>/", CartDetailView.as_view(), name="cart-detail"),
]
