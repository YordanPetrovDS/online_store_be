from rest_framework.serializers import ModelSerializer

from cms.models import Banner, Page, Paragraph


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ("id", "image", "video")


class ParagraphSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ("id", "title", "content", "image")


class PageSerializer(ModelSerializer):
    banners = BannerSerializer(many=True, read_only=True)
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = (
            "id",
            "slug",
            "title",
            "custom_javascript",
            "banners",
            "paragraphs",
            "og_image",
            "is_published",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "meta_canonical",
        )
