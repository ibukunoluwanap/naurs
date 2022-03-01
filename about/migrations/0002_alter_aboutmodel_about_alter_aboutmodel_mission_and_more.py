# Generated by Django 4.0.1 on 2022-02-25 10:45

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutmodel',
            name='about',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aboutmodel',
            name='mission',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aboutmodel',
            name='value',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aboutmodel',
            name='vision',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]