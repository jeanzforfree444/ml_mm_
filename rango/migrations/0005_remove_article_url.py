# Generated by Django 2.2.28 on 2025-02-02 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_userprofile_is_editor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='url',
        ),
    ]
