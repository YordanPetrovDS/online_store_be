from modeltranslation.translator import TranslationOptions, register

from geo.models import Country, Region, State


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(State)
class StateTranslationOptions(TranslationOptions):
    fields = ("title",)
