# Generated by Django 4.0.1 on 2022-05-07 16:34

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FreeTrialOfferModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=100, verbose_name='phone number')),
                ('is_active', models.BooleanField(default=True, verbose_name='activate')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'Free Trial Offer',
                'verbose_name_plural': 'Free Trial Offers',
            },
        ),
        migrations.CreateModel(
            name='OfferModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='offers/', verbose_name='image')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('is_active', models.BooleanField(default=True, verbose_name='activate')),
                ('content', tinymce.models.HTMLField()),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'Offer',
                'verbose_name_plural': 'Offers',
            },
        ),
        migrations.CreateModel(
            name='BookOfferModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=100, verbose_name='phone number')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.offermodel', verbose_name='offer')),
            ],
            options={
                'verbose_name': 'Booked Offer',
                'verbose_name_plural': 'Booked Offers',
            },
        ),
    ]
