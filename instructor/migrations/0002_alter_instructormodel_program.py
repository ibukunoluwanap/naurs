# Generated by Django 4.0.1 on 2022-04-07 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_alter_programbenefitmodel_program_and_more'),
        ('instructor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructormodel',
            name='program',
            field=models.ManyToManyField(to='program.ProgramModel', verbose_name='class'),
        ),
    ]
