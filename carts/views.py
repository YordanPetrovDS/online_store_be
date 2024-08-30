from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from carts.models import Cart
from carts.serializers import AddProductToCartSerializer, CartSerializer


class AddProductToCartView(CreateAPIView):
    """
    CreateAPIView to handle adding a product to the cart.
    """

    queryset = Cart.objects.all()
    serializer_class = AddProductToCartSerializer

    def create(self, request, *args, **kwargs):
        """
        Overriding the create method to customize response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        return Response({"hash": cart.hash}, status=status.HTTP_200_OK)


class CartDetailView(RetrieveAPIView):
    """
    RetrieveAPIView to get details of a specific cart by hash.
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = "hash"
