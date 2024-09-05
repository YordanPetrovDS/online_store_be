from rest_framework import viewsets

from shipping_methods.models import ShippingMethod
from shipping_methods.serializers import ShippingMethodSerializer


class ShippingMethodViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing shipping method instances.
    """

    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer
    filterset_fields = ["provider", "is_active"]
    search_fields = ["title"]
    ordering_fields = ["title", "min_price", "ship_price", "free_ship_over"]
