# Generated by Django 4.0.1 on 2022-04-15 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_programmodel_instructors_programmodel_students'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProgramPaymentModel',
        ),
    ]
