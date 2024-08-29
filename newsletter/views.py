from rest_framework import viewsets

from newsletter.models import Subscriber
from newsletter.serializers import SubscriberSerializer


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
