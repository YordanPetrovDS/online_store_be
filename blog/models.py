from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from cms.models import Page
from common.models import BaseModel
from utils.functions import get_upload_path
from utils.validators import image_validator


class ArticleCategory(BaseModel):
    title = models.CharField(max_length=64)
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("sort_order",)
        verbose_name_plural = "Article categories"


class ArticleTag(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Article Tag"
        verbose_name_plural = "Article Tags"
        ordering = ["name"]


class Article(Page):
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])
    banner = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])
    categories = models.ManyToManyField(to=ArticleCategory)
    tags = models.ManyToManyField(ArticleTag, related_name="articles", blank=True)

    def __str__(self):
        return self.title
