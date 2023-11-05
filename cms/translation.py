from modeltranslation.translator import TranslationOptions, register

from cms.models import Page, Paragraph


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = (
        "slug",
        "title",
        "custom_javascript",
        "meta_title",
        "meta_description",
        "meta_keywords",
        "meta_canonical",
        "content",
    )


@register(Paragraph)
class ParagraphTranslationOptions(TranslationOptions):
    fields = ("title", "content")
