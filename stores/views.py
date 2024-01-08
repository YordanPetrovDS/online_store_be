from rest_framework import viewsets

from stores.models import Store, StoreLocation, StoreSetting
from stores.serializers import (
    StoreLocationSerializer,
    StoreSerializer,
    StoreSettingSerializer,
)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreLocationViewSet(viewsets.ModelViewSet):
    queryset = StoreLocation.objects.all()
    serializer_class = StoreLocationSerializer


class StoreSettingViewSet(viewsets.ModelViewSet):
    queryset = StoreSetting.objects.all()
    serializer_class = StoreSettingSerializer
