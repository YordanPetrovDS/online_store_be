from rest_framework import generics

from cms.models import Page
from cms.serializers import PageSerializer
from common.mixins import ListExcludeEmptyTitleModelMixin


class PageListView(ListExcludeEmptyTitleModelMixin, generics.ListAPIView):
    queryset = Page.objects.order_by("slug")
    serializer_class = PageSerializer


class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects
    serializer_class = PageSerializer
    lookup_field = "slug"
