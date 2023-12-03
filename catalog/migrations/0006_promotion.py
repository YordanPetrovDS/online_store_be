# Generated by Django 4.1.3 on 2023-11-29 13:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_productdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField()),
                ('valid_until', models.DateTimeField()),
                ('title', models.CharField(max_length=128)),
                ('discount_percent', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('allowed_brands', models.ManyToManyField(blank=True, related_name='promotions', to='catalog.brand')),
                ('allowed_categories', models.ManyToManyField(blank=True, related_name='promotions', to='catalog.productcategory')),
                ('allowed_products', models.ManyToManyField(blank=True, related_name='promotions', to='catalog.product')),
            ],
            options={
                'ordering': ['valid_from'],
            },
        ),
    ]
