# Generated by Django 4.0.1 on 2022-03-15 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingmodel',
            name='category',
            field=models.CharField(choices=[('Music', 'Music'), ('Gymnastic', 'Gymnastic'), ('Yoga', 'Yoga'), ('Art', 'Art')], default=('Music', 'Music'), max_length=100, verbose_name='category'),
        ),
    ]