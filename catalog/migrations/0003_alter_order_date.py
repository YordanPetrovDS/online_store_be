# Generated by Django 4.1.3 on 2023-01-21 22:31

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_alter_order_options_alter_orderproduct_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
