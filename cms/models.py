from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from common.models import BaseModel
from utils.functions import get_upload_path
from utils.validators import image_validator, validate_no_spaces, video_validator


class Page(BaseModel):
    slug = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    is_published = models.BooleanField(default=False)
    custom_javascript = models.TextField(blank=True)
    og_image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])
    content = RichTextUploadingField(blank=True)

    # Meta fields for SEO
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    meta_keywords = models.TextField(validators=[validate_no_spaces])
    meta_canonical = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class Banner(BaseModel):
    is_active = models.BooleanField(default=False)
    page = models.ForeignKey(Page, on_delete=models.PROTECT, related_name="banners")
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])
    video = models.FileField(upload_to=get_upload_path, blank=True, null=True, validators=[video_validator])
    url = models.URLField(max_length=256, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"Banner #{self.sort_order} for page {self.page.title}"

    class Meta:
        ordering = ("sort_order",)


class Paragraph(BaseModel):
    page = models.ForeignKey(to=Page, on_delete=models.CASCADE, related_name="paragraphs")
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, validators=[image_validator])
    content = RichTextUploadingField(blank=True, config_name="small")
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("sort_order",)


class MainPage(Page):
    pass


class InfoPage(Page):
    pass
