# Generated by Django 4.0.1 on 2022-05-04 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('program', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(default=0.0)),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallet',
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('status', models.BooleanField(default=False, verbose_name='Payment Status')),
                ('sessions', models.PositiveIntegerField(default=0)),
                ('kids_sessions', models.PositiveIntegerField(default=0)),
                ('senior_citizen_sessions', models.PositiveIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('package', models.ManyToManyField(to='program.PackageModel', verbose_name='package')),
                ('program', models.ManyToManyField(to='program.ProgramModel', verbose_name='class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='BillingAddressModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=250, verbose_name='street address')),
                ('city_town', models.CharField(max_length=100, verbose_name='city/town')),
                ('country', models.CharField(max_length=250, verbose_name='country')),
                ('zip_code', models.CharField(max_length=50, verbose_name='zip code')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Billing Address',
                'verbose_name_plural': 'Billing Addresses',
            },
        ),
    ]
