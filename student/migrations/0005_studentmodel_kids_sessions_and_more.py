# Generated by Django 4.0.1 on 2022-04-26 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_rename_kid_studentmodel_kids'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='kids_sessions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='senior_citizen_sessions',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
