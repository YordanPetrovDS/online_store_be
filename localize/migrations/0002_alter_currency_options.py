# Generated by Django 4.1.3 on 2023-12-14 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localize', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'ordering': ['id'], 'verbose_name_plural': 'Currencies'},
        ),
    ]
