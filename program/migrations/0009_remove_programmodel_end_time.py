# Generated by Django 4.0.1 on 2022-04-09 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0008_programmodel_end_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmodel',
            name='end_time',
        ),
    ]