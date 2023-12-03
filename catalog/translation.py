from modeltranslation.translator import TranslationOptions, register

from catalog.models import Brand, Product, ProductDocument


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    pass


@register(ProductDocument)
class ProductDocumentTranslationOptions(TranslationOptions):
    fields = ("title",)
