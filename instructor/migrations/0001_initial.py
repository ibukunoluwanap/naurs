# Generated by Django 4.0.1 on 2022-05-15 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100, verbose_name='role')),
                ('about', tinymce.models.HTMLField()),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
            },
        ),
    ]
