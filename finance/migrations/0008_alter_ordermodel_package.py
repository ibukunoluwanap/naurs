# Generated by Django 4.0.1 on 2022-04-24 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0005_rename_number_of_kids_sessions_packagemodel_number_of_free_kids_sessions_and_more'),
        ('finance', '0007_remove_ordermodel_package_ordermodel_package_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='package',
            field=models.ManyToManyField(to='program.PackageModel', verbose_name='package'),
        ),
    ]
