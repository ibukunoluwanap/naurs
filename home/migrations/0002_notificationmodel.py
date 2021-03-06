# Generated by Django 4.0.1 on 2022-06-02 13:15

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_read', models.BooleanField(default=False)),
                ('message', tinymce.models.HTMLField(verbose_name='message')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentmodel', verbose_name='student')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
