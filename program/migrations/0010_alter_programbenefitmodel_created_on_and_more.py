# Generated by Django 4.0.1 on 2022-03-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0009_alter_programbenefitmodel_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programbenefitmodel',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created on'),
        ),
        migrations.AlterField(
            model_name='programenquirymodel',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created on'),
        ),
        migrations.AlterField(
            model_name='programmodel',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created on'),
        ),
    ]
