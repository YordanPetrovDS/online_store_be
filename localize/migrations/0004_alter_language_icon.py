# Generated by Django 4.1.3 on 2024-09-09 14:14

from django.db import migrations, models

import utils.functions
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('localize', '0003_rename_sign_possition_currency_sign_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=utils.functions.get_upload_path, validators=[utils.validators.image_validator]),
        ),
    ]
