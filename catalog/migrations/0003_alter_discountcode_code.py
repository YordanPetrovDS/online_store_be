# Generated by Django 4.1.3 on 2023-11-28 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_discountcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='code',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
