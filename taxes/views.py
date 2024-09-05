from rest_framework import viewsets

from taxes.models import TaxGroup
from taxes.serializers import TaxGroupSerializer


class TaxGroupViewSet(viewsets.ModelViewSet):
    queryset = TaxGroup.objects.all()
    serializer_class = TaxGroupSerializer
