# Generated by Django 3.2.16 on 2024-07-22 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20240721_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
