# Generated by Django 4.1.3 on 2024-09-16 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0006_ordertotal_orderstatuschange_orderquote'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0010_alter_productdocument_file_and_more'),
        ('accounts', '0004_userreview_created_at_userreview_deleted_at_and_more'),
        ('payments_methods', '0002_alter_paymentmethod_image'),
        ('localize', '0004_alter_language_icon'),
        ('geo', '0003_remove_state_region_state_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('issued', 'Issued'), ('revoked', 'Revoked')], default='draft', max_length=8)),
                ('issued_date_time', models.DateTimeField(blank=True, null=True)),
                ('invoice_number', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('customer_first_name', models.CharField(max_length=64)),
                ('customer_last_name', models.CharField(max_length=64)),
                ('customer_phone', models.CharField(max_length=64)),
                ('customer_email', models.EmailField(max_length=64)),
                ('customer_company_name', models.CharField(blank=True, max_length=128)),
                ('customer_company_number', models.CharField(blank=True, max_length=128)),
                ('customer_invoice_details', models.CharField(blank=True, max_length=128)),
                ('billing_address_country_title', models.CharField(blank=True, max_length=128)),
                ('billing_address_city', models.CharField(blank=True, max_length=128)),
                ('billing_address_street', models.CharField(blank=True, max_length=128)),
                ('billing_address_phone', models.CharField(blank=True, max_length=128)),
                ('billing_address_email', models.EmailField(blank=True, max_length=128)),
                ('payment_method_provider', models.CharField(blank=True, max_length=32)),
                ('payment_method_title', models.CharField(blank=True, max_length=128)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address_invoice', to='accounts.useraddress')),
                ('billing_address_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_country_invoice', to='geo.country')),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='localize.currency')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='orders.order')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='payments_methods.paymentmethod')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('subtotal', 'Subtotal'), ('tax', 'Tax'), ('shipping', 'Shipping'), ('discount', 'Discount'), ('total', 'Total')], default='subtotal', max_length=16)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sort_order', models.PositiveIntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_totals', to='invoices.invoice')),
            ],
            options={
                'verbose_name': 'Invoice Total',
                'verbose_name_plural': 'Invoice Totals',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('sku', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('sort_order', models.PositiveIntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items', to='invoices.invoice')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_items', to='catalog.product')),
            ],
            options={
                'verbose_name': 'Invoice Item',
                'verbose_name_plural': 'Invoice Items',
                'ordering': ['sort_order'],
            },
        ),
    ]