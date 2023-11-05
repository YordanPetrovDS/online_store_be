# Generated by Django 4.1.3 on 2023-11-03 13:36

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InfoPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cms.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("cms.page",),
        ),
        migrations.CreateModel(
            name="MainPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cms.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("cms.page",),
        ),
        migrations.AddField(
            model_name="page",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AddField(
            model_name="page",
            name="content_bg",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, null=True
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="content_en",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, null=True
            ),
        ),
    ]
