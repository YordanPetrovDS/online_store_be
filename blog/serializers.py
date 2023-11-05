from rest_framework.serializers import ModelSerializer, Serializer

from blog.models import Article, ArticleCategory, ArticleTag


class ArticleCategorySerializer(ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ("id", "title")


class ArticleTagSerializer(ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ("id", "name", "slug")


class ArticleSerializer(ModelSerializer):
    categories = ArticleCategorySerializer(many=True, read_only=True)
    tags = ArticleTagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "slug",
            "date",
            "title",
            "is_published",
            "content",
            "image",
            "banner",
            "categories",
            "tags",
            "og_image",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "meta_canonical",
        )


class KeysSerializer(Serializer):
    """Returns list of items keys (=slugs) for NextJS FE"""

    def to_representation(self, instance):
        return instance.slug
