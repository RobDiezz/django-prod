# Generated by Django 5.1.1 on 2025-01-20 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, verbose_name='content'),
        ),
    ]
