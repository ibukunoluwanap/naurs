# Generated by Django 4.0.1 on 2022-04-16 00:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0003_delete_programpaymentmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0002_billingaddressmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('stripe_payment_intent', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=False, verbose_name='Payment Status')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='program.programmodel', verbose_name='class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
