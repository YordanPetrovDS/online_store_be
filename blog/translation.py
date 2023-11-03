from modeltranslation.translator import TranslationOptions, register

from blog.models import Article, ArticleCategory


@register(ArticleCategory)
class ArticleCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    pass  # All translatable fields are in Page model
