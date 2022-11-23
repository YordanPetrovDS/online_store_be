from django_filters import rest_framework as filters
from rest_framework import permissions

from .pagination import CustomPagination
from .permissions import IsOwnerOrAdminReadOnly


class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering and pagination."""

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = CustomPagination
