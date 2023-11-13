from rest_framework import generics, viewsets

from blog.models import Article, ArticleCategory, ArticleTag
from blog.serializers import (
    ArticleCategorySerializer,
    ArticleSerializer,
    ArticleTagSerializer,
    KeysSerializer,
)
from common.mixins import ListExcludeEmptyTitleModelMixin


class ArticleCategoryListView(ListExcludeEmptyTitleModelMixin, generics.ListAPIView):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer


class ArticleViewSet(ListExcludeEmptyTitleModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.order_by("-date")
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    filterset_fields = ("categories",)


class ArticleKeysListView(ListExcludeEmptyTitleModelMixin, generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = KeysSerializer


class ArticleTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer
