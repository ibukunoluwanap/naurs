# Generated by Django 4.0.1 on 2022-03-26 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Music', 'Music'), ('Gymnastic', 'Gymnastic'), ('Yoga', 'Yoga'), ('Art', 'Art')], default=('Music', 'Music'), max_length=100, verbose_name='category')),
                ('listing', models.CharField(max_length=100, verbose_name='listing')),
                ('coming_soon', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'Listing',
                'verbose_name_plural': 'Listings',
            },
        ),
    ]
