# Generated by Django 4.0.1 on 2022-05-02 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_studentmodel_kids_sessions_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='kids',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='kids_sessions',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='senior_citizen',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='senior_citizen_sessions',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='sessions',
        ),
    ]