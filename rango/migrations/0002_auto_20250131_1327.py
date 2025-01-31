# Generated by Django 2.2.28 on 2025-01-31 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='picture',
            new_name='profile_picture',
        ),
        migrations.AddField(
            model_name='article',
            name='article_picture',
            field=models.ImageField(blank=True, upload_to='article_images'),
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.CharField(default='', max_length=20000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
