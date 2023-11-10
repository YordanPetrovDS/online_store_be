from django.conf import settings
from django.utils import translation
from django_filters import rest_framework as filters
from rest_framework import permissions
from rest_framework.response import Response

from .pagination import CustomPagination
from .permissions import IsOwnerOrAdminReadOnly


class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering and pagination."""

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = CustomPagination


class ListExcludeEmptyTitleModelMixin:
    """
    We override only list(), not get_queryset() or filter_quesryset(),
    because we need to keep the behaviour of get_object() which is using the same methods
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Filter by not-empty title in current language
        current_language = translation.get_language()
        if current_language is not None and current_language != settings.MODELTRANSLATION_DEFAULT_LANGUAGE:
            kwargs = {f"title_{translation.get_language()}__isnull": False}
            queryset = queryset.filter(**kwargs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
