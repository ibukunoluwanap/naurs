# Generated by Django 4.0.1 on 2022-05-02 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0006_rename_number_of_free_kids_sessions_packagemodel_kids_sessions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagemodel',
            name='sessions',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
