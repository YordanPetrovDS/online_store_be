# Generated by Django 4.1.3 on 2023-11-02 10:35

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models

import utils.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.CharField(max_length=128, unique=True)),
                ("slug_en", models.CharField(max_length=128, null=True, unique=True)),
                ("slug_bg", models.CharField(max_length=128, null=True, unique=True)),
                ("title", models.CharField(max_length=256)),
                ("title_en", models.CharField(max_length=256, null=True)),
                ("title_bg", models.CharField(max_length=256, null=True)),
                ("is_published", models.BooleanField(default=False)),
                ("custom_javascript", models.TextField(blank=True)),
                ("custom_javascript_en", models.TextField(blank=True, null=True)),
                ("custom_javascript_bg", models.TextField(blank=True, null=True)),
                (
                    "og_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        validators=[utils.validators.image_validator],
                    ),
                ),
                ("meta_title", models.CharField(max_length=255)),
                ("meta_title_en", models.CharField(max_length=255, null=True)),
                ("meta_title_bg", models.CharField(max_length=255, null=True)),
                ("meta_description", models.TextField()),
                ("meta_description_en", models.TextField(null=True)),
                ("meta_description_bg", models.TextField(null=True)),
                (
                    "meta_keywords",
                    models.TextField(validators=[utils.validators.validate_no_spaces]),
                ),
                (
                    "meta_keywords_en",
                    models.TextField(
                        null=True, validators=[utils.validators.validate_no_spaces]
                    ),
                ),
                (
                    "meta_keywords_bg",
                    models.TextField(
                        null=True, validators=[utils.validators.validate_no_spaces]
                    ),
                ),
                (
                    "meta_canonical",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                (
                    "meta_canonical_en",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                (
                    "meta_canonical_bg",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Paragraph",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=256)),
                ("title_en", models.CharField(max_length=256, null=True)),
                ("title_bg", models.CharField(max_length=256, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        validators=[utils.validators.image_validator],
                    ),
                ),
                (
                    "content",
                    ckeditor_uploader.fields.RichTextUploadingField(blank=True),
                ),
                (
                    "content_en",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True
                    ),
                ),
                (
                    "content_bg",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True
                    ),
                ),
                ("sort_order", models.PositiveIntegerField(default=0)),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paragraphs",
                        to="cms.page",
                    ),
                ),
            ],
            options={
                "ordering": ("sort_order",),
            },
        ),
        migrations.CreateModel(
            name="Banner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        validators=[utils.validators.image_validator],
                    ),
                ),
                ("video", models.FileField(blank=True, null=True, upload_to="")),
                ("url", models.URLField(blank=True, max_length=256, null=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="banners",
                        to="cms.page",
                    ),
                ),
            ],
            options={
                "ordering": ("sort_order",),
            },
        ),
    ]
