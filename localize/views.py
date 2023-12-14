from rest_framework import viewsets

from localize.models import Currency, CurrencyRate, Language
from localize.serializers import (
    CurrencyRateSerializer,
    CurrencySerializer,
    LanguageSerializer,
)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyRateViewSet(viewsets.ModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer
