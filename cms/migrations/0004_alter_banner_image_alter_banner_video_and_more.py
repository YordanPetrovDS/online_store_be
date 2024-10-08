# Generated by Django 4.1.3 on 2024-09-09 14:14

from django.db import migrations, models

import utils.functions
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_alter_banner_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.functions.get_upload_path, validators=[utils.validators.image_validator]),
        ),
        migrations.AlterField(
            model_name='banner',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=utils.functions.get_upload_path, validators=[utils.validators.video_validator]),
        ),
        migrations.AlterField(
            model_name='page',
            name='og_image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.functions.get_upload_path, validators=[utils.validators.image_validator]),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.functions.get_upload_path, validators=[utils.validators.image_validator]),
        ),
    ]
