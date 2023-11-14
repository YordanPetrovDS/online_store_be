from modeltranslation.translator import TranslationOptions, register

from catalog.models import Brand


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ("title",)
