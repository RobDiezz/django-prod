# Generated by Django 5.1.1 on 2025-01-14 19:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0010_alter_order_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='delivery address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='orders/receipts/', verbose_name='receipt'),
        ),
    ]
