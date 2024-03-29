# Generated by Django 4.1.3 on 2023-11-29 12:42

import django.db.models.deletion
from django.db import migrations, models

import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_productmultimedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('title_en', models.CharField(max_length=128, null=True, verbose_name='Title')),
                ('title_bg', models.CharField(max_length=128, null=True, verbose_name='Title')),
                ('file', models.FileField(upload_to='product_documents/', validators=[utils.validators.file_validator])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='catalog.product')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
