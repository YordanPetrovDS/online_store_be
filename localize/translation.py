from modeltranslation.translator import TranslationOptions, register

from localize.models import Currency, Language


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Currency)
class CurrencyTranslationOptions(TranslationOptions):
    fields = ("title",)
