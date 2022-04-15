# Generated by Django 4.0.1 on 2022-04-15 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('program', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instructor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('instructor', models.ManyToManyField(to='instructor.InstructorModel', verbose_name='instructor')),
                ('program', models.ManyToManyField(to='program.ProgramModel', verbose_name='class')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
    ]
