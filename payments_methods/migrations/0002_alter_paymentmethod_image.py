# Generated by Django 4.1.3 on 2024-09-09 13:56

from django.db import migrations, models

import utils.functions
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('payments_methods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.functions.get_upload_path, validators=[utils.validators.image_validator]),
        ),
    ]