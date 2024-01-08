from modeltranslation.translator import TranslationOptions, register

from stores.models import Store, StoreLocation, StoreSetting


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(StoreLocation)
class StoreLocationTranslationOptions(TranslationOptions):
    fields = ("city", "title", "address", "phone", "email")


@register(StoreSetting)
class StoreSettingTranslationOptions(TranslationOptions):
    fields = ("title",)
