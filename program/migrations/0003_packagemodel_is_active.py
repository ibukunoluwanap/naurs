# Generated by Django 4.0.1 on 2022-04-07 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_alter_programbenefitmodel_program_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagemodel',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='activate'),
        ),
    ]