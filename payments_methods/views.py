from rest_framework import viewsets

from payments_methods.models import PaymentMethod
from payments_methods.serializers import PaymentMethodSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
