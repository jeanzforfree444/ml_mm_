# Generated by Django 2.2.28 on 2025-02-14 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0009_article_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
